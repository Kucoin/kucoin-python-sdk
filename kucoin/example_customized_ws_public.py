
import asyncio
import socket
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient



async def main():
    async def deal_msg(msg):
        if msg['topic'] == '/spotMarket/level2Depth5:BTC-USDT':
            print(msg["data"])
        elif msg['topic'] == '/spotMarket/level2Depth5:KCS-USDT':
            print(f'Get KCS level3:{msg["data"]}')

    # is public
    client = WsToken()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    address = ('openapi-v2.kucoin.com',443)
    sock.connect(address)

    ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False,sock=sock)

    await ws_client.subscribe('/spotMarket/level2Depth5:BTC-USDT,KCS-USDT')
    while True:
        await asyncio.sleep(60, loop=loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
