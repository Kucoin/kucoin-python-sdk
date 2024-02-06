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

    def query_isolated_margin_trading_pair(self):
        """
        https://docs.kucoin.com/#query-isolated-margin-trading-pair-configuration
        :return:
        [
            {
                "symbol": "EOS-USDC",
                "symbolName": "EOS-USDC",
                "baseCurrency": "EOS",
                "quoteCurrency": "USDC",
                "maxLeverage": 10,
                "flDebtRatio": "0.97",
                "tradeEnable": true,
                "autoRenewMaxDebtRatio": "0.96",
                "baseBorrowEnable": true,
                "quoteBorrowEnable": true,
                "baseTransferInEnable": true,
                "quoteTransferInEnable": true
            },
            {
                "symbol": "MANA-USDT",
                "symbolName": "MANA-USDT",
                "baseCurrency": "MANA",
                "quoteCurrency": "USDT",
                "maxLeverage": 10,
                "flDebtRatio": "0.9",
                "tradeEnable": true,
                "autoRenewMaxDebtRatio": "0.96",
                "baseBorrowEnable": true,
                "quoteBorrowEnable": true,
                "baseTransferInEnable": true,
                "quoteTransferInEnable": true
            }
        ]
        """
        return self._request('GET', '/api/v1/isolated/symbols')

    def query_isolated_margin_account_info(self, balance_currency=None):
        """
        https://docs.kucoin.com/#query-isolated-margin-account-info
        :param balance_currency: [Optional] The pricing coin, currently only supports USDT, KCS, and BTC.
                                 Defaults to BTC if no value is passed.
        :type: str
        :return:
        {
            "totalConversionBalance": "3.4939947",
            "liabilityConversionBalance": "0.00239066",
            "assets": [
                {
                    "symbol": "MANA-USDT",
                    "status": "CLEAR",
                    "debtRatio": "0",
                    "baseAsset": {
                        "currency": "MANA",
                        "totalBalance": "0",
                        "holdBalance": "0",
                        "availableBalance": "0",
                        "liability": "0",
                        "interest": "0",
                        "borrowableAmount": "0"
                    },
                    "quoteAsset": {
                        "currency": "USDT",
                        "totalBalance": "0",
                        "holdBalance": "0",
                        "availableBalance": "0",
                        "liability": "0",
                        "interest": "0",
                        "borrowableAmount": "0"
                    }
                },
                {
                    "symbol": "EOS-USDC",
                    "status": "CLEAR",
                    "debtRatio": "0",
                    "baseAsset": {
                        "currency": "EOS",
                        "totalBalance": "0",
                        "holdBalance": "0",
                        "availableBalance": "0",
                        "liability": "0",
                        "interest": "0",
                        "borrowableAmount": "0"
                    },
                    "quoteAsset": {
                        "currency": "USDC",
                        "totalBalance": "0",
                        "holdBalance": "0",
                        "availableBalance": "0",
                        "liability": "0",
                        "interest": "0",
                        "borrowableAmount": "0"
                    }
                }
            ]
        }
        """
        params = {}
        if balance_currency:
            params['balanceCurrency'] = balance_currency
        return self._request('GET', '/api/v1/isolated/accounts', params=params)

    def query_single_isolated_margin_account_info(self, symbol):
        """
        https://docs.kucoin.com/#query-single-isolated-margin-account-info
        :param symbol: Trading pair, e.g.: BTC-USDT (Mandatory)
        :type: str
        :return:
        {
            "symbol": "MANA-USDT",
            "status": "CLEAR",
            "debtRatio": "0",
            "baseAsset": {
                "currency": "MANA",
                "totalBalance": "0",
                "holdBalance": "0",
                "availableBalance": "0",
                "liability": "0",
                "interest": "0",
                "borrowableAmount": "0"
            },
            "quoteAsset": {
                "currency": "USDT",
                "totalBalance": "0",
                "holdBalance": "0",
                "availableBalance": "0",
                "liability": "0",
                "interest": "0",
                "borrowableAmount": "0"
            }
        }
        """
        return self._request('GET', '/api/v1/isolated/account/{symbol}'.format(symbol=symbol))

    def create_isolated_margin_borrow_order(self, symbol, currency, size, borrow_strategy, **kwargs):
        """
        https://docs.kucoin.com/#isolated-margin-borrowing
        :param symbol: Trading pair, e.g.: BTC-USDT
        :type: str
        :param currency: Borrowed coin type
        :type: str
        :param size: Borrowed amount
        :type: float
        :param borrow_strategy: Borrowing strategy: FOK, IOC
        :type: str
        :param kwargs: maxRate, period
        :return:
        {
            "orderId": "62baad0aaafc8000014042b3",
            "currency": "USDT",
            "actualSize": "10"
        }
        """
        params = {
            'symbol': symbol,
            'currency': currency,
            'size': size,
            'borrowStrategy': borrow_strategy
        }
        if kwargs:
            params.update(kwargs)
        return self._request('POST', '/api/v1/isolated/borrow', params=params)

    def query_outstanding_repayment_records(self, **kwargs):
        """
        https://docs.kucoin.com/#query-outstanding-repayment-records
        :param kwargs: symbol, currency, pageSize, currentPage
        :return:
        {
            "currentPage": 1,
            "pageSize": 10,
            "totalNum": 6,
            "totalPage": 1,
            "items": [
                {
                    "loanId": "62aec83bb51e6f000169a3f0",
                    "symbol": "BTC-USDT",
                    "currency": "USDT",
                    "liabilityBalance": "10.02000016",
                    "principalTotal": "10",
                    "interestBalance": "0.02000016",
                    "createdAt": 1655621691869,
                    "maturityTime": 1656226491869,
                    "period": 7,
                    "repaidSize": "0",
                    "dailyInterestRate": "0.001"
                },
                {
                    "loanId": "62aa94e52a3fbb0001277fd1",
                    "symbol": "BTC-USDT",
                    "currency": "USDT",
                    "liabilityBalance": "10.05166708",
                    "principalTotal": "10",
                    "interestBalance": "0.05166708",
                    "createdAt": 1655346405447,
                    "maturityTime": 1655951205447,
                    "period": 7,
                    "repaidSize": "0",
                    "dailyInterestRate": "0.001"
                }
            ]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/isolated/borrow/outstanding', params=params)

    def query_repayment_records(self, **kwargs):
        """
        https://docs.kucoin.com/#query-repayment-records
        :param kwargs: symbol, currency, pageSize, currentPage
        :return:
        {
            "currentPage": 1,
            "pageSize": 10,
            "totalNum": 30,
            "totalPage": 3,
            "items": [
                {
                    "loanId": "628df5787818320001c79c8b",
                    "symbol": "BTC-USDT",
                    "currency": "USDT",
                    "principalTotal": "10",
                    "interestBalance": "0.07000056",
                    "repaidSize": "10.07000056",
                    "createdAt": 1653470584859,
                    "period": 7,
                    "dailyInterestRate": "0.001",
                    "repayFinishAt": 1654075506416
                },
                {
                    "loanId": "628c570f7818320001d52b69",
                    "symbol": "BTC-USDT",
                    "currency": "USDT",
                    "principalTotal": "11",
                    "interestBalance": "0.07699944",
                    "repaidSize": "11.07699944",
                    "createdAt": 1653364495783,
                    "period": 7,
                    "dailyInterestRate": "0.001",
                    "repayFinishAt": 1653969432251
                }
            ]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/isolated/borrow/repaid', params=params)

    def quick_repayment(self, symbol, currency, size, seq_strategy):
        """
        https://docs.kucoin.com/#quick-repayment
        :param symbol: Trading pair, e.g.: BTC-USDT (Mandatory)
        :type: str
        :param currency: Repayment coin type
        :type: str
        :param size: Repayment amount
        :type: float
        :param seq_strategy: Repayment sequence strategy,
                             RECENTLY_EXPIRE_FIRST: Maturity date priority (the loan with the closest maturity is repaid first),
                             HIGHEST_RATE_FIRST: Interest rate priority (the loan with the highest interest rate is repaid first)
        :type: str
        :return:None
        """
        params = {
            'symbol': symbol,
            'currency': currency,
            'size': size,
            'seqStrategy': seq_strategy
        }
        return self._request('POST', '/api/v1/isolated/repay/all', params=params)

    def single_repayment(self, symbol, currency, size, loan_id):
        """
        https://docs.kucoin.com/#single-repayment
        :param symbol: Trading pair, e.g.: BTC-USDT (Mandatory)
        :type: str
        :param currency: Repayment coin type
        :type: str
        :param size: Repayment amount
        :type: float
        :param loan_id: Trade order number; when this field is configured, the sequence strategy is invalidated
        :type: str
        :return:None
        """
        params = {
            'symbol': symbol,
            'currency': currency,
            'size': size,
            'loanId': loan_id
        }
        return self._request('POST', '/api/v1/isolated/repay/single', params=params)

    def get_etf_info(self, currency=None):
        """
        Get Leveraged Token Info
        https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-leveraged-token-info
        :param currency:  if empty query all currencies
        :return:
        {
            "success": true,
            "code": "200",
            "msg": "success",
            "retry": false,
            "data": [
              {
                  "currency": "BTCUP", //currency
                  "netAsset": 0.001,//Net worth
                  "targetLeverage": "2-4", //Target leverage
                  "actualLeverage": "2.33", //Actual leverage
                  "assetsUnderManagement": //The amount of currency issued
                  "basket": "-78.671762 XBTUSDTM" //basket information
              }
            ]
        }
        """
        params = {}
        if currency:
            params["currency"] = currency

        return self._request('GET', '/api/v3/etf/info', params=params)

    def get_margin_account_Detail(self, quoteCurrency=None, queryType=None):
        """
        Get Account Detail - Cross Margin
        https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-cross-margin
        :param quoteCurrency:  quote currency, currently only supports USDT, KCS, BTC, USDT as default
        :param queryType:  Query account type (default MARGIN), MARGIN - only query low frequency cross margin account, MARGIN_V2-only query high frequency cross margin account, ALL - consistent aggregate query with the web side
        :return:
        {
            "success": true,
            "code": "200",
            "msg": "success",
            "retry": false,
            "data": {
                "timestamp": 1669708513820,
                "currentPage": 1,
                "pageSize": 100,
                "totalNum": 1,
                "totalPage": 1,
                "items": [
                    {
                        "totalLiabilityOfQuoteCurrency": "0.976", //Total Liability in Quote Currency
                        "totalAssetOfQuoteCurrency": "1.00", //Total Assets in Quote Currency
                        "debtRatio": "0.976", //debt ratio
                        "status": "LIQUIDATION", //Position status; EFFECTIVE-effective, BANKRUPTCY-bankruptcy liquidation, LIQUIDATION-closing, REPAY-repayment, BORROW borrowing
                        "assets": [
                            {
                                "currency": "BTC",
                                "borrowEnabled": true,
                                "repayEnabled": true,
                                "transferEnabled": false,
                                "borrowed": "0.976",
                                "totalAsset": "1.00", //Total Assets
                                "available": "0.024", //Account available assets (total assets - frozen)
                                "hold": "0", //Account frozen assets
                                "maxBorrowSize": "0" //The user's remaining maximum loan amount
                            }
                        ]
                    }
                ]
            }
        }
        """
        params = {}
        if quoteCurrency:
            params["quoteCurrency"] = quoteCurrency
        if queryType:
            params["queryType"] = queryType

        return self._request('GET', '/api/v3/margin/accounts', params=params)

    def get_isolated_margin_account_detail(self, quoteCurrency=None, queryType=None, symbol=None):
        """
        Get Account Detail - Isolated Margin
        https://www.kucoin.com/docs/rest/funding/funding-overview/get-account-detail-isolated-margin
        :param quoteCurrency:  quote currency, currently only supports USDT, KCS, BTC, default is USDT
        :param symbol:  For isolated trading pairs, query all without passing
        :param queryType:  Query account type (default MARGIN), ISOLATED- - only query low frequency isolated margin account, ISOLATED_V2-only query high frequency isolated margin account, ALL - consistent aggregate query with the web side
        :return:
        {
            "code": "200000",
            "data": [
                {
                    "totalAssetOfQuoteCurrency": "3.4939947",
                    "totalLiabilityOfQuoteCurrency": "0.00239066",
                    "timestamp": 1668062174000,
                    "assets": [
                        {
                            "symbol": "MANA-USDT",
                            "debtRatio": "0",
                            "status": "BORROW",
                            "baseAsset": {
                                "currency": "MANA",
                                "borrowEnabled": true,
                                "repayEnabled": true,
                                "transferEnabled": true,
                                "borrowed": "0",
                                "totalAsset": "0",
                                "available": "0",
                                "hold": "0",
                                "maxBorrowSize": "1000"
                            },
                            "quoteAsset": {
                                "currency": "USDT",
                                "borrowEnabled": true,
                                "repayEnabled": true,
                                "transferEnabled": true,
                                "borrowed": "0",
                                "totalAsset": "0",
                                "available": "0",
                                "hold": "0",
                                "maxBorrowSize": "50000"
                            }
                        }
                    ]
                }
            ]
        }
        """
        params = {}
        if quoteCurrency:
            params["quoteCurrency"] = quoteCurrency
        if queryType:
            params["queryType"] = queryType
        if symbol:
            params["symbol"] = symbol

        return self._request('GET', '/api/v3/isolated/accounts', params=params)

    def get_margin_currencies(self, isIsolated, currency=None, symbol=None):
        """
        Get Cross/Isolated Margin Risk Limit/Currency config
        https://www.kucoin.com/docs/rest/margin-trading/margin-info/get-cross-isolated-margin-risk-limit-currency-config
        :param isIsolated:  true - isolated, false - cross ; default false
        :param symbol:  symbol, required for isolated margin accounts
        :param currency:  currency
        :return:
        // CROSS MARGIN RESPONSES
        {
            "success": true,
            "code": "200",
            "msg": "success",
            "retry": false,
            "data": [
                {
                    "timestamp": 1697783812257,
                    "currency": "XMR",
                    "borrowMaxAmount": "999999999999999999",
                    "buyMaxAmount": "999999999999999999",
                    "holdMaxAmount": "999999999999999999",
                    "borrowCoefficient": "0.5",
                    "marginCoefficient": "1",
                    "precision": 8,
                    "borrowMinAmount": "0.001",
                    "borrowMinUnit": "0.001",
                    "borrowEnabled": true
                }
            ]
        }

        // ISOLATED MARGIN RESPONSES
        {
            "success": true,
            "code": "200",
            "msg": "success",
            "retry": false,
            "data": [
                {
                    "timestamp": 1697782543851,
                    "symbol": "LUNC-USDT",
                    "baseMaxBorrowAmount": "999999999999999999",
                    "quoteMaxBorrowAmount": "999999999999999999",
                    "baseMaxBuyAmount": "999999999999999999",
                    "quoteMaxBuyAmount": "999999999999999999",
                    "baseMaxHoldAmount": "999999999999999999",
                    "quoteMaxHoldAmount": "999999999999999999",
                    "basePrecision": 8,
                    "quotePrecision": 8,
                    "baseBorrowCoefficient": "1",
                    "quoteBorrowCoefficient": "1",
                    "baseMarginCoefficient": "1",
                    "quoteMarginCoefficient": "1",
                    "baseBorrowMinAmount": null,
                    "baseBorrowMinUnit": null,
                    "quoteBorrowMinAmount": "0.001",
                    "quoteBorrowMinUnit": "0.001",
                    "baseBorrowEnabled": false,
                    "quoteBorrowEnabled": true
                }
            ]
        }
        """
        params = {"isIsolated":isIsolated}
        if currency:
            params["currency"] = currency
        if symbol:
            params["symbol"] = symbol

        return self._request('GET', '/api/v3/margin/currencies', params=params)
