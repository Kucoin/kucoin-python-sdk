
import asyncio
import socket
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient



async def main():
    async def deal_msg(msg):
        print(msg["data"])



    #is private
    client = WsToken(key='', secret='', passphrase='',
                     url='https://openapi-v2.kucoin.com')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    address = ('openapi-v2.kucoin.com',443)
    sock.connect(address)

    ws_client = await KucoinWsClient.create(None, client, deal_msg, private=True,sock=sock)
    await ws_client.subscribe('/spotMarket/tradeOrders')

    while True:
        await asyncio.sleep(60, loop=loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
