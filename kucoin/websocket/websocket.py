import asyncio
import json
import time
import websockets
from random import random
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


class ConnectWebsocket:
    MAX_RECONNECTS = 5
    MAX_RECONNECT_SECONDS = 60

    def __init__(self, loop, client, callback, private=False):
        self._loop = loop
        self._client = client
        self._callback = callback
        self._reconnect_num = 0
        self._ws_details = None
        self._connect_id = None
        self._private = private
        self._last_ping = None
        self._socket = None
        self._topics = []
        asyncio.ensure_future(self.run_forever(), loop=self._loop)

    @property
    def topics(self):
        return self._topics

    async def _run(self, event: asyncio.Event):
        keep_alive = True
        self._last_ping = time.time()  # record last ping
        self._ws_details = None
        self._ws_details = self._client.get_ws_token(self._private)
        logger.debug(self._ws_details)

        async with websockets.connect(self.get_ws_endpoint(), ssl=self.get_ws_encryption()) as socket:
            self._socket = socket
            self._reconnect_num = 0

            if not event.is_set():
                await self.send_ping()
                event.set()

            while keep_alive:
                if time.time() - self._last_ping > self.get_ws_pingtimeout():
                    await self.send_ping()
                try:
                    _msg = await asyncio.wait_for(self._socket.recv(), timeout=self.get_ws_pingtimeout())
                except asyncio.TimeoutError:
                    await self.send_ping()
                except asyncio.CancelledError:
                    logger.exception('CancelledError')
                    await self._socket.ping()
                else:
                    try:
                        msg = json.loads(_msg)
                    except ValueError:
                        logger.warning(_msg)
                    else:
                        await self._callback(msg)

    def get_ws_endpoint(self):
        if not self._ws_details:
            raise Exception("Websocket details Error")
        ws_connect_id = str(uuid4()).replace('-', '')
        token = self._ws_details['token']
        endpoint = self._ws_details['instanceServers'][0]['endpoint']
        ws_endpoint = f"{endpoint}?token={token}&connectId={ws_connect_id}"
        return ws_endpoint

    def get_ws_encryption(self):
        if not self._ws_details:
            raise Exception("Websocket details Error")
        return self._ws_details['instanceServers'][0]['encrypt']

    def get_ws_pingtimeout(self):
        if not self._ws_details:
            raise Exception("Websocket details Error")
        _timeout = int(self._ws_details['instanceServers'][0]['pingTimeout'] / 1000) - 2
        return _timeout

    async def run_forever(self):
        while True:
            await self._reconnect()

    async def _reconnect(self):
        logger.info('Websocket start connect/reconnect')

        self._reconnect_num += 1
        reconnect_wait = self._get_reconnect_wait(self._reconnect_num)
        logger.info(f'asyncio sleep reconnect_wait={reconnect_wait} s reconnect_num={self._reconnect_num}')
        await asyncio.sleep(reconnect_wait)
        logger.info(f'asyncio sleep ok')
        event = asyncio.Event()

        tasks = {
            asyncio.ensure_future(self._recover_topic_req_msg(event), loop=self._loop): self._recover_topic_req_msg,
            asyncio.ensure_future(self._run(event), loop=self._loop): self._run
        }

        while set(tasks.keys()):
            finished, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_EXCEPTION)
            exception_occur = False
            for task in finished:
                if task.exception():
                    exception_occur = True
                    logger.warning("{} got an exception {}".format(task, task.exception()))
                    for pt in pending:
                        logger.warning(f'pending {pt}')
                        try:
                            pt.cancel()
                        except asyncio.CancelledError:
                            logger.exception('CancelledError ')
                        logger.warning('cancel ok.')

            if exception_occur:
                break

        logger.warning('_reconnect over.')

    async def _recover_topic_req_msg(self, event):
        logger.info(f'recover topic event {self.topics} waiting')
        await event.wait()
        logger.info(f'recover topic event {self.topics} done.')
        for topic in self.topics:
            await self.send_message({
                'type': 'subscribe',
                'topic': topic,
                'response': True
            })
            logger.info(f'{topic} OK')

    def _get_reconnect_wait(self, attempts):
        expo = 2 ** attempts
        return round(random() * min(self.MAX_RECONNECT_SECONDS, expo - 1) + 1)

    async def send_ping(self):
        msg = {
            'id': str(int(time.time() * 1000)),
            'type': 'ping'
        }
        await self._socket.send(json.dumps(msg))
        self._last_ping = time.time()

    async def send_message(self, msg, retry_count=0):
        if not self._socket:
            if retry_count < self.MAX_RECONNECTS:
                await asyncio.sleep(1)
                await self.send_message(msg, retry_count + 1)
        else:
            msg['id'] = str(int(time.time() * 1000))
            msg['privateChannel'] = self._private
            await self._socket.send(json.dumps(msg))
