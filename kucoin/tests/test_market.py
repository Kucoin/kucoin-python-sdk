from kucoin.client import Market
from kucoin.tests.config import api_key, secret, passphrase

client = Market(key=api_key, secret=secret, passphrase=passphrase)

print(client.get_symbol_detail("BTC-USDT"))