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
- 2024 02/26
1. add Api: margin.get_interest_rates:  `Get Interest Rates <https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-interest-rates>`_.

- 2024 02/19
 1. trade.get_hf_filled_list: same to trade.get_hf_transaction_records `Get HF Filled List <https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-filled-list>`_
  - :red:`The trade.get_hf_transaction_records method will be removed at some time in the future`
 2. trade.get_hf_completed_orders: same to trade.get_filled_hf_order `Get HF Completed order list <https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-completed-order-list>`_
  - :red:`The trade.get_filled_hf_order method will be removed at some time in the future`

- 2024 02/07
 1. margin.get_etf_info: `Get Leveraged Token Info <https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-leveraged-token-info>`_.
 2. margin.get_margin_account_Detail: `Get Account Detail - Cross Margin <https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-cross-margin>`_.
 3. margin.get_isolated_margin_account_detail: `Get Account Detail - Isolated Margin <https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-isolated-margin>`_.
 4. margin.get_margin_currencies: `Get Cross/Isolated Margin Risk Limit/Currency config <https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-cross-isolated-margin-risk-limit-currency-config>`_.
 5. trade.create_oco_order: `Place Order <https://www.kucoin.com/docs/rest/spot-trading/oco-order/place-order>`_.
 6. trade.cancel_oco_order: `Cancel Order by orderId <https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-orderid>`_.
 7. trade.cancel_oco_order_by_clientOid: `Cancel Order by clientOid <https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-clientoid>`_.
 8. trade.cancel_all_oco_orders: `Cancel Multiple Orders <https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-multiple-orders>`_.
 9. trade.get_oco_order_by_orderId: `Get Order Info by orderId <https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-info-by-orderid>`_.
 10. trade.get_oco_order_by_client_oid: `Get Order Info by clientOid <https://docs.kucoin.com/spot-hf/#obtain-details-of-a-single-hf-order-using-clientoid>`_.
 11. trade.get_oco_orders: `Get Order List <https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-list>`_.
 12. trade.get_oco_order_details: `Get Order Details by orderId <https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-details-by-orderid>`_.
 13. trade.cancel_all_hf_orders: `Cancel all HF orders <https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-all-hf-orders>`_.
 14. customized websocket: ./kucoin/example_customized_ws_private.py | kucoin/example_customized_ws_public.py
  - sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
 15. set api TCP_NODELAY：After instantiating the client, you can cancel the Nagle algorithm through client.TCP_NODELAY=1 (default is 0)
  - kucoin/example_client_TCP_NODELAY.py

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
- ./kucoin/example_customized_ws_private.py
- ./kucoin/example_customized_ws_public.py
- ./kucoin/example_default_ws_public.py

