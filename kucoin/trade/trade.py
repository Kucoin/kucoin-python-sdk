from kucoin.base_request.base_request import KucoinBaseRestApi


class TradeData(KucoinBaseRestApi):

    def create_limit_margin_order(self, symbol, side, size, price, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/#place-a-margin-order
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param side: place direction buy or sell (Mandatory)
        :type: str
        :param size: amount of base currency to buy or sell (Mandatory)
        :type: str
        :param price: price per base currency (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :param kwargs:  Fill in parameters with reference documents
        :return: {
                  "orderId": "5bd6e9286d99522a52e458de",
                  "borrowSize":10.2,
                  "loanApplyId":"600656d9a33ac90009de4f6f"
                }
        """
        params = {
            'symbol': symbol,
            'size': size,
            'side': side,
            'price': price,
            'type': "limit"
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/margin/order', params=params)

    def create_market_margin_order(self, symbol, side, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/#place-a-margin-order
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param side: place direction buy or sell (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :param kwargs:  Fill in parameters with reference documents
        :return: {
                  "orderId": "5bd6e9286d99522a52e458de",
                  "borrowSize":10.2,
                  "loanApplyId":"600656d9a33ac90009de4f6f"
                }
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': "market"
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/margin/order', params=params)

    def create_limit_order(self, symbol, side, size, price, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/#place-a-new-order
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param side: place direction buy or sell (Mandatory)
        :type: str
        :param size: amount of base currency to buy or sell (Mandatory)
        :type: str
        :param price: price per base currency (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :param kwargs:  Fill in parameters with reference documents
        :return: {'orderId': '5d9ee461f24b80689797fd04'}
        """
        params = {
            'symbol': symbol,
            'size': size,
            'side': side,
            'price': price,
            'type': "limit"
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/orders', params=params)

    def create_limit_stop_order(self, symbol, side, size, price, stopPrice,  clientOid="", **kwargs):
        params = {
            'symbol': symbol,
            'size': size,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'type': "limit"
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/stop-order', params=params)

    def create_market_stop_order(self, symbol, side, stopPrice, size="", funds="", clientOid="", **kwargs):
        params = {
            'symbol': symbol,
            'side': side,
            'stopPrice': stopPrice,
            'type': "market"

        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if size:
            params['size'] = size
        elif funds:
            params['funds'] = funds
        else:
            raise Exception('Funds or size')

        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/stop-order', params=params)

    def create_market_order(self, symbol, side, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/#place-a-new-order
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param side: place direction buy or sell (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :param kwargs:  Fill in parameters with reference documents
        :return: {'orderId': '5d9ee461f24b80689797fd04'}
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': "market"
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/orders', params=params)

    def create_bulk_orders(self, symbol, orderList):
        """
        https://docs.kucoin.com/#place-bulk-orders
        :param symbol: a valid trading symbol code.
        :type: str
        :param orderList: order list
        :type: list
        :return:
        {
          "data": [
            {
              "symbol": "KCS-USDT",
              "type": "limit",
              "side": "buy",
              "price": "0.01",
              "size": "0.01",
              "funds": null,
              "stp": "",
              "stop": "",
              "stopPrice": null,
              "timeInForce": "GTC",
              "cancelAfter": 0,
              "postOnly": false,
              "hidden": false,
              "iceberge": false,
              "iceberg": false,
              "visibleSize": null,
              "channel": "API",
              "id": "611a6a309281bc000674d3c0",
              "status": "success",
              "failMsg": null,
              "clientOid": "552a8a0b7cb04354be8266f0e202e7e9"
            },
            {
              "symbol": "KCS-USDT",
              "type": "limit",
              "side": "buy",
              "price": "0.01",
              "size": "0.01",
              "funds": null,
              "stp": "",
              "stop": "",
              "stopPrice": null,
              "timeInForce": "GTC",
              "cancelAfter": 0,
              "postOnly": false,
              "hidden": false,
              "iceberge": false,
              "iceberg": false,
              "visibleSize": null,
              "channel": "API",
              "id": "611a6a309281bc000674d3c1",
              "status": "success",
              "failMsg": null,
              "clientOid": "bd1e95e705724f33b508ed270888a4a9"
            }
          ]
        }
        """
        params = {
            'symbol': symbol,
            'orderList': orderList,
        }
        return self._request('POST', '/api/v1/orders/multi', params=params)

    def cancel_client_order(self, clientId):
        """
        :param orderId: str  (Mandatory)
        :return:{"cancelledOrderId": "5f311183c9b6d539dc614db3","clientOid": "6d539dc614db3"}
        """
        return self._request('DELETE', f'/api/v1/order/client-order/{clientId}')

    def cancel_stop_order(self, orderId):
        """
        :param orderId: Order ID, unique ID of the order. (Mandatory)
        :type: str
        :return:
        {
             "cancelledOrderIds": [
              "5bd6e9286d99522a52e458de"   //orderId
            ]
        }
        """
        return self._request('DELETE', f'/api/v1/stop-order/{orderId}')

    def cancel_client_stop_order(self, clientOid, symbol=""):
        """
        :param orderId: Order ID, unique ID of the order. (Mandatory)
        :type: str
        :return:
        {
             "cancelledOrderIds": [
              "5bd6e9286d99522a52e458de"   //orderId
            ]
        }
        """
        params = {
            "clientOid": clientOid
        }
        if symbol:
            params["symbol"] = symbol

        return self._request('DELETE', f'/api/v1/stop-order/cancelOrderByClientOid', params=params)

    def cancel_stop_condition_order(self, symbol="", tradeType="", orderIds=""):
        """
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        if tradeType:
            params["tradeType"] = tradeType
        if orderIds:
            params["orderIds"] = orderIds

        return self._request('DELETE', f'/api/v1/stop-order/cancel',params=params)

    def cancel_order(self, orderId):
        """
        https://docs.kucoin.com/#cancel-an-order

        :param orderId: Order ID, unique ID of the order. (Mandatory)
        :type: str
        :return:
        {
             "cancelledOrderIds": [
              "5bd6e9286d99522a52e458de"   //orderId
            ]
        }
        """
        return self._request('DELETE', '/api/v1/orders/{orderId}'.format(orderId=orderId))

    def cancel_all_orders(self, **kwargs):
        """
        https://docs.kucoin.com/#cancel-all-orders
        :param kwargs: [optional] symbol, tradeType
        :return:
        {
           "cancelledOrderIds": [
              "5c52e11203aa677f33e493fb",  //orderId
              "5c52e12103aa677f33e493fe",
              "5c52e12a03aa677f33e49401",
              "5c52e1be03aa677f33e49404",
              "5c52e21003aa677f33e49407",
              "5c6243cb03aa67580f20bf2f",
              "5c62443703aa67580f20bf32",
              "5c6265c503aa676fee84129c",
              "5c6269e503aa676fee84129f",
              "5c626b0803aa676fee8412a2"
            ]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('DELETE', '/api/v1/orders', params=params)

    def get_order_list(self, **kwargs):
        """
        https://docs.kucoin.com/#list-orders
        :param kwargs: [optional] symbol, status, side, type, tradeType, startAt, endAt, currentPage, pageSize and so on
        :return:
        {
            "currentPage": 1,
            "pageSize": 1,
            "totalNum": 153408,
            "totalPage": 153408,
            "items": [
              {
                "id": "5c35c02703aa673ceec2a168",   //orderid
                "symbol": "BTC-USDT",   //symbol
                "opType": "DEAL",      // operation type: DEAL
                "type": "limit",       // order type,e.g. limit,market,stop_limit.
                "side": "buy",         // transaction direction,include buy and sell
                "price": "10",         // order price
                "size": "2",           // order quantity
                "funds": "0",          // order funds
                "dealFunds": "0.166",  // deal funds
                "dealSize": "2",       // deal quantity
                "fee": "0",            // fee
                "feeCurrency": "USDT", // charge fee currency
                "stp": "",             // self trade prevention,include CN,CO,DC,CB
                "stop": "",            // stop type
                "stopTriggered": false,  // stop order is triggered
                "stopPrice": "0",      // stop price
                "timeInForce": "GTC",  // time InForce,include GTC,GTT,IOC,FOK
                "postOnly": false,     // postOnly
                "hidden": false,       // hidden order
                "iceberg": false,      // iceberg order
                "visibleSize": "0",    // display quantity for iceberg order
                "cancelAfter": 0,      // cancel orders time，requires timeInForce to be GTT
                "channel": "IOS",      // order source
                "clientOid": "",       // user-entered order unique mark
                "remark": "",          // remark
                "tags": "",            // tag order source
                "isActive": false,     // status before unfilled or uncancelled
                "cancelExist": false,   // order cancellation transaction record
                "createdAt": 1547026471000,  // create time
                "tradeType": "TRADE"
              }
            ]
         }
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/orders', params=params)

    def get_recent_orders(self):
        """
        https://docs.kucoin.com/#recent-orders
        :return:
        {
            "currentPage": 1,
            "pageSize": 1,
            "totalNum": 153408,
            "totalPage": 153408,
            "items": [
              {
                "id": "5c35c02703aa673ceec2a168",
                "symbol": "BTC-USDT",
                "opType": "DEAL",
                "type": "limit",
                "side": "buy",
                "price": "10",
                "size": "2",
                "funds": "0",
                "dealFunds": "0.166",
                "dealSize": "2",
                "fee": "0",
                "feeCurrency": "USDT",
                "stp": "",
                "stop": "",
                "stopTriggered": false,
                "stopPrice": "0",
                "timeInForce": "GTC",
                "postOnly": false,
                "hidden": false,
                "iceberg": false,
                "visibleSize": "0",
                "cancelAfter": 0,
                "channel": "IOS",
                "clientOid": "",
                "remark": "",
                "tags": "",
                "isActive": false,
                "cancelExist": false,
                "createdAt": 1547026471000,
                "tradeType": "TRADE"
              }
            ]
        }
        """

        return self._request('GET', '/api/v1/limit/orders')

    def get_order_details(self, orderId):
        """
        https://docs.kucoin.com/#get-an-order
        :param orderId: Order ID, unique identifier of an order, obtained via the List orders. (Mandatory)
        :return:
        {
            "id": "5c35c02703aa673ceec2a168",
            "symbol": "BTC-USDT",
            "opType": "DEAL",
            "type": "limit",
            "side": "buy",
            "price": "10",
            "size": "2",
            "funds": "0",
            "dealFunds": "0.166",
            "dealSize": "2",
            "fee": "0",
            "feeCurrency": "USDT",
            "stp": "",
            "stop": "",
            "stopTriggered": false,
            "stopPrice": "0",
            "timeInForce": "GTC",
            "postOnly": false,
            "hidden": false,
            "iceberg": false,
            "visibleSize": "0",
            "cancelAfter": 0,
            "channel": "IOS",
            "clientOid": "",
            "remark": "",
            "tags": "",
            "isActive": false,
            "cancelExist": false,
            "createdAt": 1547026471000,
            "tradeType": "TRADE"
        }
        """
        return self._request('GET', '/api/v1/orders/{orderId}'.format(orderId=orderId))

    def get_all_stop_order_details(self, **kwargs):
        """
        :param orderId: Order ID, unique identifier of an order, obtained via the List orders. (Mandatory)
        :return:
        {
            "id": "5c35c02703aa673ceec2a168",
            "symbol": "BTC-USDT",
            "opType": "DEAL",
            "type": "limit",
            "side": "buy",
            "price": "10",
            "size": "2",
            "funds": "0",
            "dealFunds": "0.166",
            "dealSize": "2",
            "fee": "0",
            "feeCurrency": "USDT",
            "stp": "",
            "stop": "",
            "stopTriggered": false,
            "stopPrice": "0",
            "timeInForce": "GTC",
            "postOnly": false,
            "hidden": false,
            "iceberg": false,
            "visibleSize": "0",
            "cancelAfter": 0,
            "channel": "IOS",
            "clientOid": "",
            "remark": "",
            "tags": "",
            "isActive": false,
            "cancelExist": false,
            "createdAt": 1547026471000,
            "tradeType": "TRADE"
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', f'/api/v1/stop-order', params=params)

    def get_stop_order_details(self, orderId):
        """
        :param orderId: Order ID, unique identifier of an order, obtained via the List orders. (Mandatory)
        :return:
        {
            "id": "5c35c02703aa673ceec2a168",
            "symbol": "BTC-USDT",
            "opType": "DEAL",
            "type": "limit",
            "side": "buy",
            "price": "10",
            "size": "2",
            "funds": "0",
            "dealFunds": "0.166",
            "dealSize": "2",
            "fee": "0",
            "feeCurrency": "USDT",
            "stp": "",
            "stop": "",
            "stopTriggered": false,
            "stopPrice": "0",
            "timeInForce": "GTC",
            "postOnly": false,
            "hidden": false,
            "iceberg": false,
            "visibleSize": "0",
            "cancelAfter": 0,
            "channel": "IOS",
            "clientOid": "",
            "remark": "",
            "tags": "",
            "isActive": false,
            "cancelExist": false,
            "createdAt": 1547026471000,
            "tradeType": "TRADE"
        }
        """
        return self._request('GET', f'/api/v1/stop-order/{orderId}')

    def get_client_stop_order_details(self, clientOid, symbol=''):
        """
        :param orderId: Order ID, unique identifier of an order, obtained via the List orders. (Mandatory)
        :return:
        {
            "id": "5c35c02703aa673ceec2a168",
            "symbol": "BTC-USDT",
            "opType": "DEAL",
            "type": "limit",
            "side": "buy",
            "price": "10",
            "size": "2",
            "funds": "0",
            "dealFunds": "0.166",
            "dealSize": "2",
            "fee": "0",
            "feeCurrency": "USDT",
            "stp": "",
            "stop": "",
            "stopTriggered": false,
            "stopPrice": "0",
            "timeInForce": "GTC",
            "postOnly": false,
            "hidden": false,
            "iceberg": false,
            "visibleSize": "0",
            "cancelAfter": 0,
            "channel": "IOS",
            "clientOid": "",
            "remark": "",
            "tags": "",
            "isActive": false,
            "cancelExist": false,
            "createdAt": 1547026471000,
            "tradeType": "TRADE"
        }
        """
        params = {
            "clientOid": clientOid
        }
        if symbol:
            params["symbol"] = symbol

        return self._request('GET', f'/api/v1/stop-order/queryOrderByClientOid', params=params)

    def get_fill_list(self, tradeType, **kwargs):
        """
        https://docs.kucoin.com/#list-fills
        :param tradeType: The type of trading (Mandatory)
        :param kwargs: [Optional] orderId, symbol, side, type, startAt, endAt, currentPage, pageSize
        :return:
        {
            "currentPage":1,
            "pageSize":1,
            "totalNum":251915,
            "totalPage":251915,
            "items":[
                {
                    "symbol":"BTC-USDT",    //symbol
                    "tradeId":"5c35c02709e4f67d5266954e",   //trade id
                    "orderId":"5c35c02703aa673ceec2a168",   //order id
                    "counterOrderId":"5c1ab46003aa676e487fa8e3",  //counter order id
                    "side":"buy",   //transaction direction,include buy and sell
                    "liquidity":"taker",  //include taker and maker
                    "forceTaker":true,  //forced to become taker
                    "price":"0.083",   //order price
                    "size":"0.8424304",  //order quantity
                    "funds":"0.0699217232",  //order funds
                    "fee":"0",  //fee
                    "feeRate":"0",  //fee rate
                    "feeCurrency":"USDT",  // charge fee currency
                    "stop":"",        // stop type
                    "type":"limit",  // order type,e.g. limit,market,stop_limit.
                    "createdAt":1547026472000,  //time
                    "tradeType": "TRADE"
                }
            ]
        }
        """
        params = {
            'tradeType': tradeType
        }
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/fills', params=params)

    def get_recent_fills(self):
        """
        https://docs.kucoin.com/#recent-fills
        :return:
        [
            {
                "counterOrderId":"5db7ee769797cf0008e3beea",
                "createdAt":1572335233000,
                "fee":"0.946357371456",
                "feeCurrency":"USDT",
                "feeRate":"0.001",
                "forceTaker":true,
                "funds":"946.357371456",
                "liquidity":"taker",
                "orderId":"5db7ee805d53620008dce1ba",
                "price":"9466.8",
                "side":"buy",
                "size":"0.09996592",
                "stop":"",
                "symbol":"BTC-USDT",
                "tradeId":"5db7ee8054c05c0008069e21",
                "tradeType":"MARGIN_TRADE",
                "type":"market"
            },
            {
                "counterOrderId":"5db7ee4b5d53620008dcde8e",
                "createdAt":1572335207000,
                "fee":"0.94625",
                "feeCurrency":"USDT",
                "feeRate":"0.001",
                "forceTaker":true,
                "funds":"946.25",
                "liquidity":"taker",
                "orderId":"5db7ee675d53620008dce01e",
                "price":"9462.5",
                "side":"sell",
                "size":"0.1",
                "stop":"",
                "symbol":"BTC-USDT",
                "tradeId":"5db7ee6754c05c0008069e03",
                "tradeType":"MARGIN_TRADE",
                "type":"market"
            },
            {
                "counterOrderId":"5db69aa4688933000aab8114",
                "createdAt":1572248229000,
                "fee":"1.882148318525",
                "feeCurrency":"USDT",
                "feeRate":"0.001",
                "forceTaker":false,
                "funds":"1882.148318525",
                "liquidity":"maker",
                "orderId":"5db69a9c4e6d020008f03275",
                "price":"9354.5",
                "side":"sell",
                "size":"0.20120245",
                "stop":"",
                "symbol":"BTC-USDT",
                "tradeId":"5db69aa477d8de0008c1efac",
                "tradeType":"MARGIN_TRADE",
                "type":"limit"
            }
        ]
        """
        return self._request('GET', '/api/v1/limit/fills')

    def get_client_order_details(self, clientOid):
        """
        https://docs.kucoin.com/#recent-fills
        :param clientOid: Unique order id created by users to identify their orders
        :return:
        {
          "id": "61149d589281bc00064a9ee0",
          "symbol": "KCS-USDT",
          "opType": "DEAL",
          "type": "limit",
          "side": "buy",
          "price": "0.001",
          "size": "0.01",
          "funds": "0",
          "dealFunds": "0",
          "dealSize": "0",
          "fee": "0",
          "feeCurrency": "USDT",
          "stp": "",
          "stop": "",
          "stopTriggered": false,
          "stopPrice": "0",
          "timeInForce": "GTC",
          "postOnly": false,
          "hidden": false,
          "iceberg": false,
          "visibleSize": "0",
          "cancelAfter": 0,
          "channel": "API",
          "clientOid": "03cd879961b64429b0e0149f311ce59f",
          "remark": null,
          "tags": null,
          "isActive": false,
          "cancelExist": true,
          "createdAt": 1628740952556,
          "tradeType": "MARGIN_TRADE"
        }
        """
        return self._request('GET', f'/api/v1/order/client-order/{clientOid}')