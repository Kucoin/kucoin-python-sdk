===============================
Welcome to python-kucoin-sdk
===============================

.. image:: https://img.shields.io/pypi/l/python-kucoin
    :target: https://github.com/Kucoin/kucoin-python-sdk/blob/master/LICENSE

.. image:: https://img.shields.io/badge/python-3.6%2B-green
    :target: https://pypi.org/project/python-kucoin


Features
--------

- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling
- Implement websockets (note only python3.6+)

update
----------
- 2020 12/01

Quick Start
-----------

Register an account with `KuCoin <https://www.kucoin.com/ucenter/signup>`_.

To test on the Sandbox  with `KuCoin Sandbox <https://sandbox.kucoin.com/>`_.

`Generate an API Key <https://www.kucoin.com/account/api>`_
or `Generate an API Key in Sandbox <https://sandbox.kucoin.com/account/api>`_ and enable it.

.. code:: bash

    pip install kucoin-python

.. code:: python

    #  MarketData
    from kucoin.client import Market
    client = Market(url='https://api.kucoin.com')
    # client = Market()

    # or connect to Sandbox
    # client = Market(url='https://openapi-sandbox.kucoin.com')
    # client = Market(is_sandbox=True)

    # get symbol kline
    klines = client.get_kline('BTC-USDT','1min')

    # get symbol ticker
    server_time = client.get_server_timestamp()

    api_key = '<api_key>'
    api_secret = '<api_secret>'
    api_passphrase = '<api_passphrase>'

    # Trade
    from kucoin.client import Trade
    client = Trade(key='', secret='', passphrase='', is_sandbox=False, url='')

    # or connect to Sandbox
    # client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)

    # place a limit buy order
    order_id = client.create_limit_order('BTC-USDT', 'buy', '1', '8000')

    # place a market buy order   Use cautiously
    order_id = client.create_market_order('BTC-USDT', 'buy', size='1')

    # cancel limit order 
    client.cancel_order('5bd6e9286d99522a52e458de')

    # User
    from kucoin.client import User
    client = User(api_key, api_secret, api_passphrase)

    # or connect to Sandbox
    # client = User(api_key, api_secret, api_passphrase, is_sandbox=True)

    address = client.get_withdrawal_quota('KCS')

Websockets
----------

.. code:: python

    import asyncio
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
        #is private
        # client = WsToken(key='', secret='', passphrase='', is_sandbox=False, url='')
        # is sandbox
        # client = WsToken(is_sandbox=True)
        ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)
        # await ws_client.subscribe('/market/ticker:BTC-USDT,ETH-USDT')
        await ws_client.subscribe('/spotMarket/level2Depth5:BTC-USDT,KCS-USDT')
        while True:
            await asyncio.sleep(60, loop=loop)


    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
