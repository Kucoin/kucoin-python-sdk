from kucoin.base_request.base_request import KucoinBaseRestApi


class MarginData(KucoinBaseRestApi):

    def get_mark_price(self, symbol):
        """
        https://docs.kucoin.com/#margin-info
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
            "symbol": "USDT-BTC",
            "granularity": 5000,
            "timePoint": 1568701710000,
            "value": 0.00009807
        }
        """
        return self._request('GET', '/api/v1/mark-price/{symbol}/current'.format(symbol=symbol))

    def get_margin_config(self):
        """
        https://docs.kucoin.com/#get-margin-configuration-info
        :return:
        {
            "currencyList": ["BTC","USDT","EOS"],
            "warningDebtRatio": "0.8",
            "liqDebtRatio": "0.9",
            "maxLeverage": "3"
        }
        """
        return self._request('GET', '/api/v1/margin/config')

    def get_margin_account(self):
        """
        https://docs.kucoin.com/#get-margin-account
        :return:
        {
            "accounts": [
              {
                "availableBalance": "990.11",
                "currency": "USDT",
                "holdBalance": "7.22",
                "liability": "66.66",
                "maxBorrowSize": "88.88",
                "totalBalance": "997.33"
              }
            ],
            "debtRatio": "0.33"
        }
        """
        return self._request('GET', '/api/v1/margin/account')

    def create_borrow_order(self, currency, order_type, size, **kwargs):
        """
        https://docs.kucoin.com/#post-borrow-order
        :param currency: Currency to Borrow (Mandatory)
        :type: str
        :param order_type: Type: FOK, IOC (Mandatory)
        :type: str
        :param size: Total size (Mandatory)
        :type: float
        :param kwargs: [Optional] maxRate, term
        :return:
        {
            "orderId": "a2111213",
            "currency": "USDT"
        }
        """
        params = {
            'currency': currency,
            'type': order_type,
            'size': size,
        }
        if kwargs:
            params.update(kwargs)
        return self._request('POST', '/api/v1/margin/borrow', params=params)

    def get_borrow_order(self, orderId):
        """
        https://docs.kucoin.com/#get-borrow-order
        :param orderId: Borrow order ID
        :type: str
        :return:
        {
            "currency": "USDT",
            "filled": 1.009,
            "matchList": [
              {
                "currency": "USDT",
                "dailyIntRate": "0.001",
                "size": "12.9",
                "term": 7,
                "timestamp": "1544657947759",
                "tradeId": "1212331"
              }
            ],
            "orderId": "a2111213",
            "size": "1.009",
            "status": "DONE"
          }
        """
        params = {
            'orderId': orderId
        }

        return self._request('GET', '/api/v1/margin/borrow', params=params)

    def get_repay_record(self, **kwargs):
        """
        https://docs.kucoin.com/#get-repay-record
        :param kwargs: [Optional] currency, currentPage, pageSize
        :return:
        {
            "currentPage": 0,
            "items": [
              {
                "accruedInterest": "0.22121",
                "createdAt": "1544657947759",
                "currency": "USDT",
                "dailyIntRate": "0.0021",
                "liability": "1.32121",
                "maturityTime": "1544657947759",
                "principal": "1.22121",
                "repaidSize": "0",
                "term": 7,
                "tradeId": "1231141"
              }
            ],
            "pageSize": 0,
            "totalNum": 0,
            "totalPage": 0
          }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/margin/borrow/outstanding', params=params)

    def get_repayment_record(self, **kwargs):
        """
        https://docs.kucoin.com/#get-repayment-record
        :param kwargs: [Optional] currency, currentPage, pageSize
        :return:
        {
            "currentPage": 0,
            "items": [
              {
                "currency": "USDT",
                "dailyIntRate": "0.0021",
                "interest": "0.22121",
                "principal": "1.22121",
                "repaidSize": "0",
                "repayTime": "1544657947759",
                "term": 7,
                "tradeId": "1231141"
              }
            ],
            "pageSize": 0,
            "totalNum": 0,
            "totalPage": 0
          }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/margin/borrow/repaid', params=params)

    def click_to_repayment(self, currency, sequence, size):
        """
        https://docs.kucoin.com/#one-click-repayment
        :param currency: currency (Mandatory)
        :type: str
        :param sequence: Repayment strategy. (Mandatory)
        RECENTLY_EXPIRE_FIRST: Time priority, namely to repay the loans of the nearest maturity time first,
        HIGHEST_RATE_FIRST: Rate Priority: Repay the loans of the highest interest rate first.
        :type: str
        :param size: Repayment size (Mandatory)
        :type: float
        :return:
        """
        params = {
            'currency': currency,
            'sequence': sequence,
            'size': size
        }
        return self._request('POST', '/api/v1/margin/repay/all', params=params)

    def repay_single_order(self, currency, tradeId, size):
        """
        https://docs.kucoin.com/#repay-a-single-order
        :param currency: currency (Mandatory)
        :type: str
        :param tradeId: Trade ID (Mandatory)
        :type: str
        :param size: Repayment size (Mandatory)
        :type: float
        :return:
        """
        params = {
            'currency': currency,
            'tradeId': tradeId,
            'size': size
        }
        return self._request('POST', '/api/v1/margin/repay/single', params=params)

    def create_lend_order(self, currency, size, dailyIntRate, term):
        """
        https://docs.kucoin.com/#post-lend-order
        :param currency: Currency to lend (Mandatory)
        :type: str
        :param size: Total size (Mandatory)
        :type: str
        :param dailyIntRate: Daily interest rate. e.g. 0.002 is 0.2% (Mandatory)
        :type: str
        :param term: Term (Unit: Day) (Mandatory)
        :type: int
        :return:
        {
            "orderId": "5da5a4f0f943c040c2f8501e"
        }
        """
        params = {
            'currency': currency,
            'size': size,
            'dailyIntRate': dailyIntRate,
            'term': term
        }
        return self._request('POST', '/api/v1/margin/lend', params=params)

    def cancel_lend_order(self, orderId):
        """
        https://docs.kucoin.com/#cancel-lend-order
        :param orderId: Lend order ID (Mandatory)
        :type: str
        :return:
        """
        return self._request('DELETE', '/api/v1/margin/lend/{orderId}'.format(orderId=orderId))

    def set_auto_lend(self, currency, isEnable, **kwargs):
        """
        https://docs.kucoin.com/#set-auto-lend
        :param currency: currency (Mandatory)
        :type: str
        :param isEnable: Auto-lend enabled or not (Mandatory)
        :type: bool
        :param kwargs: [Required when isEnable is true] retainSize, dailyIntRate, term
        :return:
        """
        params = {
            'currency': currency,
            'isEnable': isEnable
        }
        if kwargs:
            params.update(kwargs)
        return self._request('POST', '/api/v1/margin/toggle-auto-lend', params=params)

    def get_active_order(self, **kwargs):
        """
        https://docs.kucoin.com/#get-active-order
        :param kwargs: [Optional] currency, currentPage, pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 1,
            "totalNum": 1,
            "totalPage": 1,
            "items": [{
                "orderId": "5da59f5ef943c033b2b643e4",
                "currency": "BTC",
                "size": "0.51",
                "filledSize": "0",
                "dailyIntRate": "0.0001",
                "term": 7,
                "createdAt": 1571135326913
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/margin/lend/active', params=params)

    def get_lent_history(self, **kwargs):
        """
        https://docs.kucoin.com/#get-lent-history
        :param kwargs: [Optional] currency, currentPage, pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 1,
            "totalNum": 1,
            "totalPage": 1,
            "items": [{
                "orderId": "5da59f5bf943c033b2b643da",
                "currency": "BTC",
                "size": "0.51",
                "filledSize": "0.51",
                "dailyIntRate": "0.0001",
                "term": 7,
                "createdAt": 1571135323984,
                "status": "FILLED"
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/margin/lend/done', params=params)

    def get_active_list(self, **kwargs):
        """
        https://docs.kucoin.com/#get-active-lend-order-list
        :param kwargs: [Optional] currency, currentPage, pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 1,
            "totalNum": 1,
            "totalPage": 1,
            "items": [{
                "tradeId": "5da6dba0f943c0c81f5d5db5",
                "currency": "BTC",
                "size": "0.51",
                "accruedInterest": "0",
                "repaid": "0.10999968",
                "dailyIntRate": "0.0001",
                "term": 14,
                "maturityTime": 1572425888958
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/margin/lend/trade/unsettled', params=params)

    def get_settled_order(self, **kwargs):
        """
        https://docs.kucoin.com/#get-settled-lend-order-history
        :param kwargs: [Optional] currency, currentPage, pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 1,
            "totalNum": 1,
            "totalPage": 1,
            "items": [{
                "tradeId": "5da59fe6f943c033b2b6440b",
                "currency": "BTC",
                "size": "0.51",
                "interest": "0.00004899",
                "repaid": "0.510041641",
                "dailyIntRate": "0.0001",
                "term": 7,
                "settledAt": 1571216254767,
                "note": "The account of the borrowers reached a negative balance, and the system has supplemented the loss via the insurance fund. Deposit funds: 0.51."
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/margin/lend/trade/settled', params=params)

    def get_lend_record(self, currency=None):
        """
        https://docs.kucoin.com/#get-account-lend-record
        :param currency: currency (Optional)
        :type: str
        :return:
        [{
            "currency": "BTC",
            "outstanding": "1.02",
            "filledSize": "0.91000213",
            "accruedInterest": "0.00000213",
            "realizedProfit": "0.000045261",
            "isAutoLend": false
        }]
        """
        params = {}
        if currency:
            params['currency'] = currency
        return self._request('GET', '/api/v1/margin/lend/assets', params=params)

    def get_lending_market(self, currency, term=None):
        """
        https://docs.kucoin.com/#lending-market-data
        :param currency: currency (Mandatory)
        :type: str
        :param term: Term (Unit: Day) (Optional)
        :type: int
        :return:
        [{
            "dailyIntRate": "0.0001",
            "term": 7,
            "size": "1.02"
        }]
        """
        params = {
            'currency': currency
        }
        if term:
            params['term'] = term
        return self._request('GET', '/api/v1/margin/market', params=params)

    def get_margin_data(self, currency):
        """
        https://docs.kucoin.com/#margin-trade-data
        :param currency: currency (Mandatory)
        :type: str
        :return:
        [{
            "tradeId": "5da6dba0f943c0c81f5d5db5",
            "currency": "BTC",
            "size": "0.51",
            "dailyIntRate": "0.0001",
            "term": 14,
            "timestamp": 1571216288958989641
        }]
        """
        params = {
            'currency': currency
        }
        return self._request('GET', '/api/v1/margin/trade/last', params=params)
    
    def get_margin_risk_limit(self, marginModel='cross'):
        """
        https://docs.kucoin.com/#margin-trade-data
        :param marginModel: marginModel
        :type: str
        :return:
        [{
        "currency": "BTC",
        "borrowMaxAmount": "50",
        "buyMaxAmount": "50",
        "precision": 8
        },
        {
        "currency": "SKL",
        "borrowMaxAmount": "50000",
        "buyMaxAmount": "51000",
        "precision": 3
        },
        {
        "currency": "USDT",
        "borrowMaxAmount": "100000",
        "buyMaxAmount": "10000000000",
        "precision": 8
        },
        {
        "currency": "ETH",
        "borrowMaxAmount": "236",
        "buyMaxAmount": "500",
        "precision": 8
        },
        {
        "currency": "LTC",
        "borrowMaxAmount": "100",
        "buyMaxAmount": "40",
        "precision": 8
        }]
        """
        params = {
            'marginModel': marginModel,
        }
        return self._request('GET', '/api/v1/risk/limit/strategy', params=params)

