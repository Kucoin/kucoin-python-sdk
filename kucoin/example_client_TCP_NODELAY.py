

#  MarginData
from kucoin.client import Trade
import time


client = Trade(key='', secret='', passphrase='',
               url='https://openapi-v2.kucoin.com')
#client.TCP_NODELAY=1
res=client.create_oco_order('FRM-USDT','buy','0.05','0.09','25','0.08','',"mark")
res2=client.cancel_oco_order(res['orderId'])
print(res)
print(res2)
