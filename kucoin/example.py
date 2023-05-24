# User
from kucoin.client import User

client = User(key='', secret='', passphrase='',
              url='https://openapi-v2.kucoin.com')

user_page = client.get_sub_user_page()
print(user_page)

account_summary_info = client.get_account_summary_info()
print(account_summary_info)

create_sub_account_res = client.create_sub_account(password='password1234', sub_name='test123456', access='Spot')
print(create_sub_account_res)

create_apis_for_sub_account_res = client.create_apis_for_sub_account(sub_name='test123456',
                                                                     passphrase='password1234', remark='apiRemark')
print(create_apis_for_sub_account_res)
sub_account_api_list = client.get_sub_account_api_list(sub_name='test123456')
print(sub_account_api_list)

modify_apis_for_sub_account_res = client.modify_sub_account_apis(sub_name='test123456', passphrase='password1234',
                                                                 api_key='')
print(modify_apis_for_sub_account_res)
sub_account_api_list = client.get_sub_account_api_list(sub_name='test123456')
print(sub_account_api_list)

delete_apis_for_sub_account_res = client.delete_sub_account_apis(sub_name='test123456', passphrase='password1234',
                                                                 api_key='')
print(delete_apis_for_sub_account_res)

sub_account_page_info = client.get_sub_account_page_info()
print(sub_account_page_info)

hf_account_ledgers = client.get_hf_account_ledgers()
print(hf_account_ledgers)

hf_account = client.transfer_to_hf_account(client_oid='oid', currency='USDT', from_payer='trade', amount=1.0)
print(hf_account)

#  MarketData
from kucoin.client import Market

client = Market(key='', secret='', passphrase='',
                url='https://openapi-v2.kucoin.com')

# get symbol kline
symbol_list = client.get_symbol_list_v2()
print(symbol_list)

# MarginData
from kucoin.client import Margin

client = Margin(key='', secret='', passphrase='',
                url='https://openapi-v2.kucoin.com')

isolated_margin_trading_pair = client.query_isolated_margin_trading_pair()
print(isolated_margin_trading_pair)

isolated_margin_account_info = client.query_isolated_margin_account_info('USDT')
print(isolated_margin_account_info)

single_isolated_margin_account_info = client.query_single_isolated_margin_account_info('BTC-USDT')
print(single_isolated_margin_account_info)

create_isolated_margin_borrow_order_res = client.create_isolated_margin_borrow_order(symbol='BTC-USDT', currency='USDT',
                                                                                     size=10.0, borrow_strategy='FOK')
print(create_isolated_margin_borrow_order_res)

outstanding_repayment_records = client.query_outstanding_repayment_records()
print(outstanding_repayment_records)

repayment_records = client.query_repayment_records()
print(repayment_records)

quick_repayment_res = client.quick_repayment(symbol='BTC-USDT', currency='USDT', size=10.0,
                                             seq_strategy='RECENTLY_EXPIRE_FIRST')
print(quick_repayment_res)

single_repayment_res = client.single_repayment(symbol='BTC-USDT', currency='USDT', size=10.0,
                                               loan_id='6465def80248d60001e23872')
print(single_repayment_res)

#  MarginData
from kucoin.client import Trade

client = Trade(key='', secret='', passphrase='',
               url='https://openapi-v2.kucoin.com')

create_limit_hf_order_res = client.create_limit_hf_order(symbol='BTC-USDT', side='buy', size='1.0', price='111')
print(create_limit_hf_order_res)

create_market_hf_order_res = client.create_hf_market_order(symbol='BTC-USDT', side='buy', size='1.0')
print(create_market_hf_order_res)

sync_create_limit_hf_order_res = client.sync_create_limit_hf_order(symbol='BTC-USDT', side='buy', size='1.0',
                                                                   price='111')
print(sync_create_limit_hf_order_res)

sync_create_market_hf_order_res = client.sync_create_hf_market_order(symbol='BTC-USDT', side='buy', size='1.0')
print(sync_create_market_hf_order_res)

orderList = [
    {
        'clientOid': '3d07008668054da6b3cb12e432c2b13a',
        'side': 'buy',
        'type': 'limit',
        'price': '1',
        'size': '1',
        'symbol': 'ETH-USDT'
    },
    {
        'clientOid': '3d07008668054da6b3cb12e432c2b13a',
        'side': 'buy',
        'type': 'limit',
        'price': '1',
        'size': '1',
        'symbol': 'ETH-USDT'
    }
]

multi_create_hf_order_res = client.multi_create_hf_order(orderList)
print(multi_create_hf_order_res)

sync_multi_create_hf_order_res = client.sync_multi_create_hf_order(orderList)
print(sync_multi_create_hf_order_res)

modify_hf_order_res = client.modify_hf_order(symbol='BTC-USDT', newPrice='1')
print(modify_hf_order_res)

cancel_hf_order_by_order_id_res = client.cancel_hf_order_by_order_id(symbol='BTC-USDT',
                                                                     orderId='3d07008668054da6b3cb12e432c2b13a')
print(cancel_hf_order_by_order_id_res)

sync_cancel_hf_order_by_order_id_res = client.sync_cancel_hf_order_by_order_id(symbol='BTC-USDT',
                                                                               orderId='3d07008668054da6b3cb12e432c2b13a')
print(sync_cancel_hf_order_by_order_id_res)

cancel_hf_order_by_client_oid_res = client.cancel_hf_order_by_client_id(symbol='BTC-USDT',
                                                                        clientOid='3d07008668054da6b3cb12e432c2b13a')
print(cancel_hf_order_by_client_oid_res)

sync_cancel_hf_order_by_client_oid_res = client.sync_cancel_hf_order_by_client_id(symbol='BTC-USDT',
                                                                                  clientOid='3d07008668054da6b3cb12e432c2b13a')
print(sync_cancel_hf_order_by_client_oid_res)

cancel_hf_order_specified_number_by_order_id_res = client.cancel_hf_order_specified_number_by_order_id(
    symbol='BTC-USDT', orderId='orderId', cancelSize='10.01')
print(cancel_hf_order_specified_number_by_order_id_res)

cancel_all_hf_orders_res = client.cancel_all_hf_orders(symbol='BTC-USDT')
print(cancel_all_hf_orders_res)

active_hf_orders = client.get_active_hf_orders(symbol='BTC-USDT')
print(active_hf_orders)

symbol_with_active_hf_orders = client.get_symbol_with_active_hf_orders()
print(symbol_with_active_hf_orders)

filled_hf_order = client.get_filled_hf_order(symbol='BTC-USDT')
print(filled_hf_order)

single_hf_order_by_client_oid = client.get_single_hf_order_by_client_oid(symbol='BTC-USDT', clientOid='clientOid')
print(single_hf_order_by_client_oid)

set_hf_auto_cancel_res = client.set_hf_auto_cancel(timeout=5)
print(set_hf_auto_cancel_res)

hf_auto_cancel_setting = client.query_hf_auto_cancel_setting()
print(hf_auto_cancel_setting)

hf_transaction_records = client.get_hf_transaction_records(symbol='BTC-USDT')
print(hf_transaction_records)
