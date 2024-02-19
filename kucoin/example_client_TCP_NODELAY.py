

#  MarginData
from kucoin.client import Trade
import time


client = Trade(key='5c2db93503aa674c74a31734', secret='f03a5284-5c39-4aaa-9b20-dea10bdcf8e3', passphrase='QWIxMjM0NTY3OCkoKiZeJSQjQA==',
               url='https://openapi-v2.kucoin.com')
#client.TCP_NODELAY=1
res=client.create_oco_order('FRM-USDT','buy','0.05','0.09','25','0.08','',"mark")
res2=client.cancel_oco_order(res['orderId'])
print(res)
print(res2)
