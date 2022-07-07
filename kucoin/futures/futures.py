from kucoin.base_request.base_request import KucoinBaseRestApi


class FuturesData(KucoinBaseRestApi):

    def __init__(self, key='', secret='', passphrase='', is_sandbox=False, url='', is_v1api=False):
        super().__init__(key, secret, passphrase, is_sandbox, url, is_v1api)
        # Change url
        self.url = 'http://api-futures.kucoin.com'

    def account_overview(self, currency=None):
        """
        https://docs.kucoin.com/futures/?lang=en_US#get-account-overview
        :param currency: [Optional] Currecny, including XBT, USDT, Default XBT
        :type: str
        :return:
        { 
            "code": "200000",
            "data": {
                "accountEquity": 99.8999305281, //Account equity = marginBalance + Unrealised PNL 
                "unrealisedPNL": 0, //Unrealised profit and loss
                "marginBalance": 99.8999305281, //Margin balance = positionMargin + orderMargin + frozenFunds + availableBalance - unrealisedPNL
                "positionMargin": 0, //Position margin
                "orderMargin": 0, //Order margin
                "frozenFunds": 0, //Frozen funds for withdrawal and out-transfer
                "availableBalance": 99.8999305281 //Available balance
                "currency": "XBT" //currency code
            }
        }
        """
        if currency is None:
            return self._request('GET', '/api/v1/account-overview')
        return self._request('GET', '/api/v1/account-overview?currency=' + currency)


    # To do: Add all the other methods
