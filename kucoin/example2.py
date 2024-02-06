

#  MarginData
from kucoin.client import Trade


client = Trade(key='', secret='', passphrase='',
               url='https://openapi-v2.kucoin.com')

res=client.create_oco_order('FRM-USDT','buy','0.05','0.09','25','0.08','',"mark")
print(res)