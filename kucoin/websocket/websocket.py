import asyncio
import json
import time
import websockets
from random import random


class ConnectWebsocket:
    MAX_RECONNECTS = 5
    MAX_RECONNECT_SECONDS = 60

    def __init__(self, loop, client, callback, private=False):
        self._loop = loop
        self._client = client
        self._callback = callback
        self._reconnect_num = 0
        self._conn = None
        self._ws_details = None
        self._connect_id = None
        self._private = private
        self._last_ping = None
        self._socket = None
        self._connect()

    def _connect(self):
        self._conn = asyncio.ensure_future(self._run(), loop=self._loop)

    async def _run(self):
        keep_alive = True
        self._last_ping = time.time()  # record last ping
        self._ws_details = None
        self._ws_details = self._client.get_ws_token(self._private)

        async with websockets.connect(self.get_ws_endpoint(), ssl=self.get_ws_encryption()) as socket:
            self._socket = socket
            self._reconnect_num = 0
            try:
                while keep_alive:
                    if time.time() - self._last_ping > self.get_ws_pingtimeout():
                        await self.send_ping()
                    try:
                        _msg = await asyncio.wait_for(self._socket.recv(), timeout=self.get_ws_pingtimeout())
                    except asyncio.TimeoutError:
                        await self.send_ping()
                    except asyncio.CancelledError:
                        await self._socket.ping()
                    else:
                        try:
                            msg = json.loads(_msg)
                        except ValueError:
                            pass
                        else:
                            await self._callback(msg)
            except websockets.ConnectionClosed:
                await self._reconnect()
            except Exception as e:
                await self._reconnect()

    def get_ws_endpoint(self):
        if not self._ws_details:
            raise Exception("Websocket details Error")
        ws_connect_id = str(int(time.time() * 1000))
        token = self._ws_details['token']
        endpoint = self._ws_details['instanceServers'][0]['endpoint']
        ws_endpoint = f"{endpoint}?token={token}&connectId={ws_connect_id}"
        if self._private:
            ws_endpoint += '&acceptUserMessage=true'
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

    async def _reconnect(self):
        await self.cancel()
        self._reconnect_num += 1
        if self._reconnect_num < self.MAX_RECONNECTS:
            reconnect_wait = self._get_reconnect_wait(self._reconnect_num)
            await asyncio.sleep(reconnect_wait)
            self._connect()
        else:
            raise Exception(f"Websocket Could Not Reconnect After :{self._reconnect_num}")

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
            if retry_count < 5:
                await asyncio.sleep(1)
                await self.send_message(msg, retry_count + 1)
        else:
            msg['id'] = str(int(time.time() * 1000))
            msg['privateChannel'] = self._private
            await self._socket.send(json.dumps(msg))

    async def cancel(self):
        try:
            self._conn.cancel()
        except asyncio.CancelledError:
            raise Exception('Cancel Connect Error')
