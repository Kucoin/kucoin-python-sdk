import warnings
from kucoin.base_request.base_request import KucoinBaseRestApi


class MarketData(KucoinBaseRestApi):

    def get_symbol_list(self, **kwargs):
        """
        https://docs.kucoin.com/#get-symbols-list
        :param kwargs: [Optional] market
        :return:
        [
          {
            "symbol": "BTC-USDT",
            "name": "BTC-USDT",
            "baseCurrency": "BTC",
            "quoteCurrency": "USDT",
            "baseMinSize": "0.00000001",
            "quoteMinSize": "0.01",
            "baseMaxSize": "10000",
            "quoteMaxSize": "100000",
            "baseIncrement": "0.00000001",
            "quoteIncrement": "0.01",
            "priceIncrement": "0.00000001",
            "feeCurrency": "USDT",
            "enableTrading": true,
            "isMarginEnabled": true,
            "priceLimitRate": "0.1"
          }
        ]
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/symbols', params=params)

    def get_ticker(self, symbol):
        """
        https://docs.kucoin.com/#get-ticker
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
            "sequence": "1550467636704",
            "bestAsk": "0.03715004",
            "size": "0.17",
            "price": "0.03715005",
            "bestBidSize": "3.803",
            "bestBid": "0.03710768",
            "bestAskSize": "1.788",
            "time": 1550653727731

        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v1/market/orderbook/level1', params=params)

    def get_all_tickers(self):
        """
        https://docs.kucoin.com/#get-all-tickers
        :return:
        {
            "time": 1550653727731,
            "ticker": [
              {
                "symbol": "BTC-USDT",
                "symbolName": "BTC-USDT",
                "buy": "0.00001191",
                "sell": "0.00001206",
                "changeRate": "0.057",
                "changePrice": "0.00000065",
                "high": "0.0000123",
                "low": "0.00001109",
                "vol": "45161.5073",
                "volValue": "2127.28693026”,
                "last": "0.00001204"
              },
              {
                "symbol": "BCD-BTC",
                "symbolName": "BCD-BTC",
                "buy": "0.00018564",
                "sell": "0.0002",
                "changeRate": "-0.0753",
                "changePrice": "-0.00001522",
                "high": "0.00021489",
                "low": "0.00018351",
                "vol": "72.99679763",
                "volValue": "2127.28693026”,
                "last": "0.00018664"
              }
            ]
        }
        """
        return self._request('GET', '/api/v1/market/allTickers')

    def get_24h_stats(self, symbol):
        """
        https://docs.kucoin.com/#get-24hr-stats
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
            "symbol": "ETH-BTC",    // symbol
            "high": "0.03736329",   // 24h highest price
            "vol": "2127.286930263025",  // 24h volume，the aggregated trading volume in ETH
            "volValue": "43.58567564",  // 24h total, the trading volume in quote currency of last 24 hours
            "last": "0.03713983",   // last price
            "low": "0.03651252",    // 24h lowest price
            "buy": "0.03712118",    // bestAsk
            "sell": "0.03713983",   // bestBid
            "changePrice": "0.00037224",  // 24h change price
            "averagePrice": "8699.24180977",//24h average transaction price yesterday
            "time": 1550847784668,  //time
            "changeRate": "0.0101" // 24h change rate
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v1/market/stats', params=params)

    def get_market_list(self):
        """
        https://docs.kucoin.com/#get-market-list
        :return:
        [
            "BTC",
            "KCS",
            "USDS",  //SC has been changed to USDS
            "ALTS" //ALTS market includes ETH, NEO, TRX
        ]
        """
        return self._request('GET', '/api/v1/markets')

    def get_part_order(self, pieces, symbol):
        """
        https://docs.kucoin.com/#get-part-order-book-aggregated
        :param pieces: pieces of data (ask and bid data) on the order book (Mandatory)
        :type: int
        :param symbol: symbol
        :type: str
        :return:
        {
            "sequence": "3262786978",
            "time": 1550653727731,
            "bids": [["6500.12", "0.45054140"],
                     ["6500.11", "0.45054140"]],  //[price，size]
            "asks": [["6500.16", "0.57753524"],
                     ["6500.15", "0.57753524"]]
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v1/market/orderbook/level2_{pieces}'.format(pieces=pieces), params=params)

    def get_aggregated_orderv3(self, symbol):
        """
        https://docs.kucoin.com/#get-full-order-book-aggregated
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
            "sequence": "3262786978",
            "time": 1550653727731,
            "bids": [["6500.12", "0.45054140"],
                     ["6500.11", "0.45054140"]],  //[price，size]
            "asks": [["6500.16", "0.57753524"],
                     ["6500.15", "0.57753524"]]
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v3/market/orderbook/level2', params=params)

    def get_aggregated_order(self, symbol):
        """
        https://docs.kucoin.com/#get-full-order-book-aggregated
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
            "sequence": "3262786978",
            "time": 1550653727731,
            "bids": [["6500.12", "0.45054140"],
                     ["6500.11", "0.45054140"]],  //[price，size]
            "asks": [["6500.16", "0.57753524"],
                     ["6500.15", "0.57753524"]]
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v2/market/orderbook/level2', params=params)

    def get_atomic_orderv3(self, symbol):
        """
        https://docs.kucoin.com/#get-full-order-book-atomic
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
            "data": {
                "sequence": "1573503933086",
                "asks": [
                    [
                        "5e0d672c1f311300093ac522",   //orderId
                        "0.1917",                     //price
                        "390.9275",                   //size
                        "1577936689346546088"         //time,nanoseconds
                    ],
                    [
                        "5e0d672891432f000819ecc3",
                        "0.19171",
                        "1456.1316",
                        "1577936685718811031"
                    ]
                ],
                "bids": [
                    [
                        "5e0d672cdc53860007f30262",
                        "0.19166",
                        "178.1936",
                        "1577936689166023452"
                    ],
                    [
                        "5e0d671a91432f000819d1b0",
                        "0.19165",
                        "583.6298",
                        "1577936671595901518"
                    ]
                ],
                "time": 1577936685107
            }
        }
        """
        return self._request('GET', f'/api/v3/market/orderbook/level3?symbol={symbol}')

    def get_atomic_order(self, symbol):
        """
        https://docs.kucoin.com/#get-full-order-book-atomic
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        {
            "data": {
                "sequence": "1573503933086",
                "asks": [
                    [
                        "5e0d672c1f311300093ac522",   //orderId
                        "0.1917",                     //price
                        "390.9275",                   //size
                        "1577936689346546088"         //time,nanoseconds
                    ],
                    [
                        "5e0d672891432f000819ecc3",
                        "0.19171",
                        "1456.1316",
                        "1577936685718811031"
                    ]
                ],
                "bids": [
                    [
                        "5e0d672cdc53860007f30262",
                        "0.19166",
                        "178.1936",
                        "1577936689166023452"
                    ],
                    [
                        "5e0d671a91432f000819d1b0",
                        "0.19165",
                        "583.6298",
                        "1577936671595901518"
                    ]
                ],
                "time": 1577936685107
            }
        }
        """
        return self._request('GET', f'/api/v1/market/orderbook/level3?symbol={symbol}')

    def get_trade_histories(self, symbol):
        """
        https://docs.kucoin.com/#get-trade-histories
        :param symbol: symbol (Mandatory)
        :type: str
        :return:
        [
          {
              "sequence": "1545896668571",
              "price": "0.07",                      //Filled price
              "size": "0.004",                      //Filled amount
              "side": "buy",                        //Filled side. The filled side is set to the taker by default.
              "time": 1545904567062140823           //Transaction time
          },
          {
              "sequence": "1545896668578",
              "price": "0.054",
              "size": "0.066",
              "side": "buy",
              "time": 1545904581619888405
          }
        ]
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v1/market/histories', params=params)

    def get_kline(self, symbol, kline_type, **kwargs):
        """
        https://docs.kucoin.com/#get-klines
        :param symbol: symbol (Mandatory)
        :type: str
        :param kline_type: Type of candlestick patterns (Mandatory)
        :type: str
        :param kwargs: [Optional] startAt, endAt, currentPage, pageSize
        :return:
        [
          [
              "1545904980",             //Start time of the candle cycle
              "0.058",                  //opening price
              "0.049",                  //closing price
              "0.058",                  //highest price
              "0.049",                  //lowest price
              "0.018",                  //Transaction amount
              "0.000945"                //Transaction volume
          ],
          [
              "1545904920",
              "0.058",
              "0.072",
              "0.072",
              "0.058",
              "0.103",
              "0.006986"
          ]
        ]
        """
        params = {
            'symbol': symbol,
            'type': kline_type
        }
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/market/candles', params=params)

    def get_currencies(self):
        """
        https://docs.kucoin.com/#get-currencies
        :return:
        [{
            "currency": "BTC",
            "name": "BTC",
            "fullName": "Bitcoin",
            "precision": 8,
            "withdrawalMinSize": "0.002",
            "withdrawalMinFee": "0.0005",
            "isWithdrawEnabled": true,
            "isDepositEnabled": true,
            "isMarginEnabled": true,
            "isDebitEnabled": true
        },
        {

            "currency": "ETH",
            "name": "ETH",
            "fullName": "Ethereum",
            "precision": 8,
            "withdrawalMinSize": "0.02",
            "withdrawalMinFee": "0.01",
            "isWithdrawEnabled": true,
            "isDepositEnabled": true,
            "isMarginEnabled": true,
            "isDebitEnabled": true

        }]
        """
        return self._request('GET', '/api/v1/currencies')

    def get_currency_detail(self, currency, chain=None):
        """
        https://docs.kucoin.com/#get-currency-detail
        :param currency: currency (Mandatory)
        :type: str
        :param chain: [Optional] Support for querying the chain of currency, e.g. The available value for USDT are OMNI,
        ERC20, TRC20. This only apply for multi-chain currency, and there is no need for single chain currency.
        :type: str
        :return:
        {
            "currency": "BTC",
            "name": "BTC",
            "fullName": "Bitcoin",
            "precision": 8,
            "withdrawalMinSize": "0.002",
            "withdrawalMinFee": "0.0005",
            "isWithdrawEnabled": true,
            "isDepositEnabled": true,
            "isMarginEnabled": true,
            "isDebitEnabled": true
        }
        """
        warnings.warn("The 'get_currency_detail' method is deprecated, use 'get_currency_detail_v2' instead",
                      DeprecationWarning)
        params = {}
        if chain:
            params['chain'] = chain
        return self._request('GET', '/api/v1/currencies/{currency}'.format(currency=currency), params=params)
    
    def get_currency_detail_v2(self, currency, chain=None):
        """
        https://docs.kucoin.com/#get-currency-detail-recommend
        :param currency: currency (Mandatory)
        :type: str
        :param chain: [Optional] Support for querying the chain of currency, return the currency details of all chains by default.
        :type: str
        :return:
        {
          "currency": "BTC",
          "name": "BTC",
          "fullName": "Bitcoin",
          "precision": 8,
          "confirms": null,
          "contractAddress": null,
          "isMarginEnabled": true,
          "isDebitEnabled": true,
          "chains": [
            {
              "chainName": "BTC",
              "withdrawalMinSize": "0.0008",
              "withdrawalMinFee": "0.0005",
              "isWithdrawEnabled": true,
              "isDepositEnabled": true,
              "confirms": 2,
              "contractAddress": ""
            },
            {
              "chainName": "KCC",
              "withdrawalMinSize": "0.0008",
              "withdrawalMinFee": "0.00002",
              "isWithdrawEnabled": true,
              "isDepositEnabled": true,
              "confirms": 20,
              "contractAddress": ""
            },
            {
              "chainName": "TRC20",
              "withdrawalMinSize": "0.0008",
              "withdrawalMinFee": "0.0004",
              "isWithdrawEnabled": false,
              "isDepositEnabled": true,
              "confirms": 1,
              "contractAddress": ""
            },
            {
              "chainName": "BTC-Segwit",
              "withdrawalMinSize": "0.0008",
              "withdrawalMinFee": "0.0005",
              "isWithdrawEnabled": true,
              "isDepositEnabled": true,
              "confirms": 2,
              "contractAddress": ""
            }
          ]
        }
        """
        params = {}
        if chain:
            params['chain'] = chain
        return self._request('GET', '/api/v2/currencies/{currency}'.format(currency=currency), params=params)
    

    def get_fiat_price(self, **kwargs):
        """
        https://docs.kucoin.com/#get-fiat-price
        :param kwargs: [Optional] base, currencies
        :return:
        {
            "BTC": "3911.28000000",
            "ETH": "144.55492453",
            "LTC": "48.45888179",
            "KCS": "0.45546856"
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/prices', params=params)

    def get_server_timestamp(self):
        """
        https://docs.kucoin.com/#server-time

        get server timestamp
        :return: 1570609496404
        """
        return self._request('GET', '/api/v1/timestamp', auth=False)

    def get_server_status(self):
        """
        https://docs.kucoin.com/#server-time

        get server timestamp
        :return:
        {
          "status": "open",                //open, close, cancelonly
          "msg":  "upgrade match engine"   //remark for operation
        }
        """
        return self._request('GET', '/api/v1/status', auth=False)
