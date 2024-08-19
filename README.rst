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
- 2024 08/19
1. 【FIX】 Fix the issue with incorrect fields in the parameters.

- 2024 07/25
1. 【NEW】GET /api/v3/hf/margin/order/active/symbols: Margin.get_active_hf_order_symbols
2. 【NEW】GET /api/v3/margin/symbols: Margin.get_cross_margin_trading_pairs_configuration
3. 【NEW】POST /api/v3/position/update-user-leverage: Margin.modify_leverage_multiplier
4. 【NEW】GET /api/v1/otc-loan/loan: Margin.get_information_onoff_exchange_funding_and_loans
5. 【NEW】GET /api/v1/otc-loan/accounts: Margin.get_information_on_accounts_involved_in_off_exchange_loans
6. 【UPDATE】POST /api/v3/margin/borrow -add isHf: Margin.margin_borrowing
7. 【UPDATE】POST /api/v3/margin/repay -add isHf: Margin.repayment
8. 【NEW】POST /api/v3/hf/margin/order: Margin.place_hf_order
9. 【NEW】POST /api/v3/hf/margin/order/test: Margin.place_hf_order_test
10. 【NEW】DELETE /api/v3/hf/margin/orders/{orderId}: Margin.cancel_hf_order_by_orderid
11. 【NEW】DELETE /api/v3/hf/margin/orders/client-order/{clientOid}: Margin.cancel_hf_order_by_clientoid
12. 【NEW】DELETE /api/v3/hf/margin/orders: Margin.cancel_all_hf_orders_by_symbol
13. 【NEW】GET /api/v3/hf/margin/orders/active: Margin.get_active_hf_orders_list
14. 【NEW】GET /api/v3/hf/margin/orders/done: Margin.get_hf_filled_list
15. 【NEW】GET /api/v3/hf/margin/orders/{orderId}: Margin.get_hf_order_details_by_orderid
16. 【NEW】GET /api/v3/hf/margin/orders/client-order/{clientOid}: Margin.get_hf_order_details_by_clientoid
17. 【NEW】GET /api/v3/hf/margin/fills: Margin.get_hf_transaction_records
18. 【NEW】GET /api/v3/currencies/{currency}: Market.get_currency_detail_v3


- 2024 07/07
1. [NEW] POST /api/v1/earn/orders: Earn.subscribe_to_earn_fixed_income_products
2. [NEW] DELETE /api/v1/earn/orders: Earn.redeem_by_earn_holding_id
3. [NEW] GET /api/v1/earn/redeem-preview: Earn.get_earn_redeem_preview_by_holding_id
4. [NEW] GET /api/v1/earn/saving/products: Earn.get_earn_savings_products
5. [NEW] GET /api/v1/earn/hold-assets: Earn.get_earn_fixed_income_current_holdings
6. [NEW] GET /api/v1/earn/promotion/products: Earn.get_earn_limited_time_promotion_products
7. [NEW] GET /api/v1/earn/kcs-staking/products: Earn.get_earn_kcs_staking_products
8. [NEW] GET /api/v1/earn/staking/products: Earn.get_earn_staking_products
9. [NEW] GET /api/v1/earn/eth-staking/products: Earn.get_earn_eth_staking_products

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
- ./kucoin/example/example_customized_ws_private.py
- ./kucoin/example/example_default_ws_public.py

