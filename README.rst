===============================
Notice: SDK Deprecation
===============================

Thank you for your support and usage of this SDK. We want to inform you that **this project is no longer actively maintained or updated**. 

To ensure you have access to the latest features, improvements, and support, we recommend transitioning to our new SDK: [**KuCoin Universal SDK**](https://github.com/Kucoin/kucoin-universal-sdk).

The KuCoin Universal SDK offers:
- A unified architecture across multiple programming languages.
- Enhanced performance and stability.
- Continued support and updates.

We appreciate your understanding and encourage you to migrate to the new SDK for a better development experience. Should you have any questions or require assistance, feel free to reach out to us.


===============================
Welcome to python-kucoin-sdk
===============================

.. image:: https://img.shields.io/pypi/l/python-kucoin
    :target: https://github.com/Kucoin/kucoin-python-sdk/blob/master/LICENSE

.. image:: https://img.shields.io/badge/python-3.6%2B-green
    :target: https://pypi.org/project/python-kucoin



.. role:: red
    :class: red

.. raw:: html

    <style>
    .red {color:IndianRed;}
    </style>

Features
--------

- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling
- Implement websockets (note only python3.6+)

update
----------
https://github.com/Kucoin/kucoin-python-sdk/releases

Quick Start
-----------

Register an account with `KuCoin <https://www.kucoin.com/ucenter/signup>`_.


`Generate an API Key <https://www.kucoin.com/account/api>`_ and enable it.

.. code:: bash

    pip install kucoin-python

.. code:: python

    #  MarketData
    from kucoin.client import Market
    client = Market(url='https://api.kucoin.com')
    # client = Market()



    # get symbol kline
    klines = client.get_kline('BTC-USDT','1min')

    # get symbol ticker
    server_time = client.get_server_timestamp()

    api_key = '<api_key>'
    api_secret = '<api_secret>'
    api_passphrase = '<api_passphrase>'

    # Trade
    from kucoin.client import Trade
    client = Trade(key='', secret='', passphrase='', url='')



    # place a limit buy order
    order_id = client.create_limit_order('BTC-USDT', 'buy', '1', '8000')

    # place a market buy order   Use cautiously
    order_id = client.create_market_order('BTC-USDT', 'buy', size='1')

    # cancel limit order 
    client.cancel_order('5bd6e9286d99522a52e458de')

    # User
    from kucoin.client import User
    client = User(api_key, api_secret, api_passphrase)



    address = client.get_withdrawal_quota('KCS')

Websockets
----------
- ./kucoin/example/example_customized_ws_private.py
- ./kucoin/example/example_default_ws_public.py

