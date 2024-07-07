[![image](https://img.shields.io/pypi/l/python-kucoin)](https://github.com/Kucoin/kucoin-python-sdk/blob/master/LICENSE)
[![image](https://img.shields.io/badge/python-3.6%2B-green)](https://pypi.org/project/python-kucoin)

# Features

-   Implementation of REST endpoints
-   Simple handling of authentication
-   Response exception handling
-   Implement websockets (note only python3.6+)

# update

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


- 2024 04/14
1. [NEW] POST /api/v3/accounts/universal-transfer:  User.flex_transfer
2. [DEPRECATED] Margin.create_borrow_order，use Margin.margin_borrowing instead
3. [DEPRECATED] Margin.get_borrow_order，use Margin.get_margin_borrowing_history instead
4. [DEPRECATED] Margin.get_repayment_record
5. [DEPRECATED] Margin.click_to_repayment，use Margin.repayment instead
6. [DEPRECATED] Margin.repay_single_order，use Margin.repayment instead
7. [DEPRECATED] Margin.create_lend_order
8. [DEPRECATED] Margin.cancel_lend_order
9. [DEPRECATED] Margin.set_auto_lend
10. [DEPRECATED] Margin.get_active_order
11. [DEPRECATED] Margin.get_lent_history
12. [DEPRECATED] Margin.get_active_list
13. [DEPRECATED] Margin.get_settled_order
14. [DEPRECATED] Margin.get_lend_record
15. [DEPRECATED] Margin.get_lending_market
16. [DEPRECATED] Margin.get_margin_data
17. [DEPRECATED] Margin.create_isolated_margin_borrow_order，use Margin.margin_borrowing instead
18. [DEPRECATED] Margin.quick_repayment，use Margin.repayment instead
19. [DEPRECATED] Margin.single_repayment，use Margin.repayment instead
20. [DEPRECATED] Margin.query_repayment_records
21. [DEPRECATED] Margin.query_outstanding_repayment_records，use Margin.query_single_isolated_margin_account_info instead
22. [DEPRECATED] Margin.get_repay_record，use Margin.get_margin_account instead

- 2024 02/26
1. add Api: margin.get_interest_rates:[Get Interest Rates](https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-interest-rates).

- 2024 02/19  
1. trade.get_hf_filled_list: same to trade.get_hf_transaction_records [Get HF Filled List](https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-filled-list)  
   - <span style="color:IndianRed;">The trade.get_hf_transaction_records method will
       be removed at some time in the future</span>

2. trade.get_hf_completed_orders: same to trade.get_filled_hf_order [Get HF Completed order list](https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/get-hf-completed-order-list)  
   - <span style="color:IndianRed;">The trade.get_filled_hf_order method will be
       removed at some time in the future</span>

- 2024 02/07  
1.  margin.get_etf_info: [Get Leveraged Token Info](https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-leveraged-token-info).
2.  margin.get_margin_account_Detail: [Get Account Detail - Cross Margin](https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-cross-margin).
3.  margin.get_isolated_margin_account_detail: [Get Account Detail - Isolated
  Margin](https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-isolated-margin).
4.  margin.get_margin_currencies: [Get Cross/Isolated Margin Risk
  Limit/Currency
  config](https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-cross-isolated-margin-risk-limit-currency-config).
5.  trade.create_oco_order: [Place
  Order](https://www.kucoin.com/docs/rest/spot-trading/oco-order/place-order).
6.  trade.cancel_oco_order: [Cancel Order by
  orderId](https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-orderid).
7.  trade.cancel_oco_order_by_clientOid: [Cancel Order by
  clientOid](https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-clientoid).
8.  trade.cancel_all_oco_orders: [Cancel Multiple
  Orders](https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-multiple-orders).
9.  trade.get_oco_order_by_orderId: [Get Order Info by
  orderId](https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-info-by-orderid).
10. trade.get_oco_order_by_client_oid: [Get Order Info by
  clientOid](https://docs.kucoin.com/spot-hf/#obtain-details-of-a-single-hf-order-using-clientoid).
11. trade.get_oco_orders: [Get Order
   List](https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-list).
12. trade.get_oco_order_details: [Get Order Details by
   orderId](https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-details-by-orderid).
13. trade.cancel_all_hf_orders: [Cancel all HF
   orders](https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-all-hf-orders).
14. customized websocket: ./kucoin/example_customized_ws_private.py \| kucoin/example_customized_ws_public.py  
-   sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

15. set api TCP_NODELAY：After instantiating the client, you can cancel the Nagle algorithm through client.TCP_NODELAY=1 (default is 0)  
-   kucoin/example_client_TCP_NODELAY.py

# Quick Start

Register an account with
[KuCoin](https://www.kucoin.com/ucenter/signup).



[Generate an API Key](https://www.kucoin.com/account/api) and enable it.

``` bash
pip install kucoin-python
```

``` python
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
```

# Websockets

-   ./kucoin/example_customized_ws_private.py
-   ./kucoin/example_customized_ws_public.py
-   ./kucoin/example_default_ws_public.py
