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

    def create_limit_stop_order(self, symbol, side, size, price, stopPrice, clientOid="", **kwargs):
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

        return self._request('DELETE', f'/api/v1/stop-order/cancel', params=params)

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

    def create_limit_hf_order(self, symbol, side, size, price, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#place-hf-order
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

        return self._request('POST', '/api/v1/hf/orders', params=params)

    def create_hf_market_order(self, symbol, side, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#place-hf-order
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

        return self._request('POST', '/api/v1/hf/orders', params=params)

    def sync_create_limit_hf_order(self, symbol, side, size, price, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#sync-place-hf-order
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
        :return:
        {
            "orderId": "6d539dc614db3",
            "orderTime": "1507725176595",//order time
            "originSize": "10.01",
            "dealSize": "2.01",
            "remainSize": "8",
            "canceledSize": "0",
            "status": "open", //open: the order is active: the order has been completed
            "matchTime": "1507725176595" //begin match time
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

        return self._request('POST', '/api/v1/hf/orders/sync', params=params)

    def sync_create_hf_market_order(self, symbol, side, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#sync-place-hf-order
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param side: place direction buy or sell (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :param kwargs:  Fill in parameters with reference documents
        :return:
        {
            "orderId": "6d539dc614db3",
            "orderTime": "1507725176595",//order time
            "originSize": "10.01",
            "dealSize": "2.01",
            "remainSize": "8",
            "canceledSize": "0",
            "status": "open", //open: the order is active: the order has been completed
            "matchTime": "1507725176595" //begin match time
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

        return self._request('POST', '/api/v1/hf/orders/sync', params=params)

    def multi_create_hf_order(self, orderList):
        """
        https://docs.kucoin.com/spot-hf/#place-multiple-hf-orders
        :param orderList: order list
        :type: list
        :return:
        [
          {
              "orderId": "641d669c9ca34800017a2a3c",
              "success": true
          },
          {
              "orderId": "641d669c9ca34800017a2a45",
              "success": true
          }
        ]
        """
        params = {
            'orderList': orderList
        }
        return self._request('POST', '/api/v1/hf/orders/multi', params=params)

    def sync_multi_create_hf_order(self, orderList):
        """
        https://docs.kucoin.com/spot-hf/#sync-place-multiple-hf-orders
        :param orderList: order list
        :type: list
        :return:
        [
          {
              "orderId": "641d67ea162d47000160bfb8",
              "orderTime": 1679648746796,
              "originSize": "1",
              "dealSize": "0",
              "remainSize": "1",
              "canceledSize": "0",
              "status": "open",
              "matchTime": 1679648746443,
              "success": true
          },
          {
              "orderId": "641d67eb162d47000160bfc0",
              "orderTime": 1679648747369,
              "originSize": "1",
              "dealSize": "0",
              "remainSize": "1",
              "canceledSize": "0",
              "status": "open",
              "matchTime": 1679648746644,
              "success": true
          }
        ]
        """
        params = {
            'orderList': orderList
        }
        return self._request('POST', '/api/v1/hf/orders/multi/sync', params=params)

    def modify_hf_order(self, symbol, clientOid='', **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#modify-order
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :param kwargs:  Fill in parameters with reference documents
        :return:
        {
            "newOrderId": "6d539dc614db3"
        }
        """
        params = {
            'symbol': symbol
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/hf/orders/alter', params=params)

    def cancel_hf_order_by_order_id(self, symbol, orderId):
        """
        https://docs.kucoin.com/spot-hf/#cancel-orders-by-orderid
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param orderId: Path parameter，Order Id unique identifier (Mandatory)
        :type: str
        :return:
        {
            "orderId": "6d539dc614db3"
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('DELETE', '/api/v1/hf/orders/{orderId}'.format(orderId=orderId), params=params)

    def sync_cancel_hf_order_by_order_id(self, symbol, orderId):
        """
        https://docs.kucoin.com/spot-hf/#sync-cancel-orders-by-orderid
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param orderId: Path parameter，Order Id unique identifier (Mandatory)
        :type: str
        :return:
        {
            "orderId": "641d67ea162d47000160bfb8",
            "originSize": "1",
            "dealSize": "0",
            "remainSize": "1",
            "canceledSize": "0",
            "status": "done"
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('DELETE', '/api/v1/hf/orders/sync/{orderId}'.format(orderId=orderId), params=params)

    def cancel_hf_order_by_client_id(self, symbol, clientOid):
        """
        https://docs.kucoin.com/spot-hf/#cancel-order-by-clientoid
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param clientOid: Path parameter，an identifier created by the (Mandatory)
        :type: str
        :return:
        {
            "clientOid": "6d539dc614db3"
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('DELETE', '/api/v1/hf/orders/client-order/{clientOid}'.format(clientOid=clientOid), params=params)

    def sync_cancel_hf_order_by_client_id(self, symbol, clientOid):
        """
        https://docs.kucoin.com/spot-hf/#sync-cancel-orders-by-clientoid
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param clientOid: Path parameter，an identifier created by the (Mandatory)
        :type: str
        :return:
        {
            "orderId": "641d67ea162d47000160bfb8",
            "originSize": "1",
            "dealSize": "0",
            "remainSize": "1",
            "canceledSize": "0",
            "status": "done"
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('DELETE', '/api/v1/hf/orders/sync/client-order/{clientOid}'.format(clientOid=clientOid), params=params)

    def cancel_hf_order_specified_number_by_order_id(self, symbol, orderId, cancelSize):
        """
        https://docs.kucoin.com/spot-hf/#cancel-specified-number-of-orders-by-orderid
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param orderId: Order id of the cancelled order
        :type: str
        :param cancelSize: canceled size
        :type: str
        :return:
        {
            "orderId": "6d539dc614db3",
            "cancelSize": "10.01"
        }
        """
        params = {
            'symbol': symbol,
            'cancelSize': cancelSize
        }
        return self._request('DELETE', '/api/v1/hf/orders/cancel/{orderId}'.format(orderId=orderId), params=params)

    def cancel_all_hf_orders(self, symbol):
        """
        https://docs.kucoin.com/spot-hf/#cancel-all-hf-orders-by-symbol
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :return: "success"
        """
        params = {
            'symbol': symbol
        }
        return self._request('DELETE', '/api/v1/hf/orders', params=params)

    def get_active_hf_orders(self, symbol):
        """
        https://docs.kucoin.com/spot-hf/#obtain-list-of-active-hf-orders
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :return:
        [
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
            "active": true,
            "inOrderBook": true,
            "cancelExist": false,
            "createdAt": 1547026471000,
            "lastUpdatedAt": 1547026471001,
            "tradeType": "TRADE",
            "cancelledSize": "0",
            "cancelledFunds": "0",
            "remainSize": "0",
            "remainFunds": "0"
            }
        ]
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v1/hf/orders/active', params=params)

    def get_symbol_with_active_hf_orders(self):
        """
        https://docs.kucoin.com/spot-hf/#obtain-list-of-symbol-with-active-hf-orders
        :return:
        {
            "symbols": ["BTC-USDT"]
        }
        """
        return self._request('GET', '/api/v1/hf/orders/active/symbols')

    def get_filled_hf_order(self, symbol, **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#obtain-list-of-filled-hf-orders
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param kwargs:  Fill in parameters with reference documents
        :return:
        {
          "lastId":2682265600,
          "items":[
             {
                "id":"63074a5a27ecbe0001e1f3ba",
                "symbol":"CSP-USDT",
                "opType":"DEAL",
                "type":"limit",
                "side":"sell",
                "price":"0.1",
                "size":"0.1",
                "funds":"0.01",
                "dealSize":"0",
                "dealFunds":"0",
                "fee":"0",
                "feeCurrency":"USDT",
                "stp":"",
                "timeInForce":"GTC",
                "postOnly":false,
                "hidden":false,
                "iceberg":false,
                "visibleSize":"0",
                "cancelAfter":0,
                "channel":"API",
                "clientOid":"",
                "remark":"",
                "tags":"",
                "cancelExist":true,
                "createdAt":1661422170924,
                "lastUpdatedAt":1661422196926,
                "tradeType":"TRADE",
                "inOrderBook":false,
                "active":false,
                "cancelledSize": "0",
                "cancelledFunds": "0",
                "remainSize": "0",
                "remainFunds": "0"
             }
          ]
        }
        """
        params = {
            'symbol': symbol
        }
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/hf/orders/done', params=params)

    def get_single_hf_order(self, symbol, orderId):
        """
        https://docs.kucoin.com/spot-hf/#details-of-a-single-hf-order
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param orderId: Order id of the cancelled order
        :type: str
        :return:
        {
            "id": "5f3113a1c9b6d539dc614dc6",
            "symbol": "KCS-BTC",
            "opType": "DEAL",
            "type": "limit",
            "side": "buy",
            "price": "0.00001",
            "size": "1",
            "funds": "0",
            "dealFunds": "0",
            "dealSize": "0",
            "fee": "0",
            "feeCurrency": "BTC",
            "stp": "",
            "timeInForce": "GTC",
            "postOnly": false,
            "hidden": false,
            "iceberg": false,
            "visibleSize": "0",
            "cancelAfter": 0,
            "channel": "API",
            "clientOid": "6d539dc614db312",
            "remark": "",
            "tags": "",
            "active": true,
            "inOrderBook": false,
            "cancelExist": false,
            "createdAt": 1547026471000,
            "lastUpdatedAt": 1547026471001,
            "tradeType": "TRADE",
            "cancelledSize": "0",
            "cancelledFunds": "0",
            "remainSize": "0",
            "remainFunds": "0"
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v1/hf/orders/{orderId}'.format(orderId=orderId), params=params)

    def get_single_hf_order_by_client_oid(self, symbol, clientOid):
        """
        https://docs.kucoin.com/spot-hf/#obtain-details-of-a-single-hf-order-using-clientoid
        :param symbol: a valid trading symbol code (Mandatory)
        :type: str
        :param clientOid: Path parameter，an identifier created by the client
        :type: str
        :return:
        {
            "id": "5f3113a1c9b6d539dc614dc6",
            "symbol": "KCS-BTC",
            "opType": "DEAL",
            "type": "limit",
            "side": "buy",
            "price": "0.00001",
            "size": "1",
            "funds": "0",
            "dealFunds": "0",
            "dealSize": "0",
            "fee": "0",
            "feeCurrency": "BTC",
            "stp": "",
            "timeInForce": "GTC",
            "postOnly": false,
            "hidden": false,
            "iceberg": false,
            "visibleSize": "0",
            "cancelAfter": 0,
            "channel": "API",
            "clientOid": "6d539dc614db312",
            "remark": "",
            "tags": "",
            "active": true,
            "inOrderBook": false,
            "cancelExist": false,
            "createdAt": 1547026471000,
            "lastUpdatedAt": 1547026471001,
            "tradeType": "TRADE",
            "cancelledSize": "0",
            "cancelledFunds": "0",
            "remainSize": "0",
            "remainFunds": "0"
        }
        """
        params = {
            'symbol': symbol
        }
        return self._request('GET', '/api/v1/hf/orders/client-order/{clientOid}'.format(clientOid=clientOid), params=params)

    def set_hf_auto_cancel(self, timeout, **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#hf-auto-cancel-setting
        :param timeout: Auto cancel order trigger setting time, the unit is second.
                        range: timeout=-1 (meaning unset) or 5 <= timeout <= 86400. For example,
                        timeout=5 means that the order will be automatically canceled if no user request is received for more than 5 seconds.
                        When this parameter is changed, the previous setting will be overwritten. (Mandatory)
        :param kwargs:  Fill in parameters with reference documents
        :return:
        {
            "currentTime": 1682010526,
            "triggerTime": 1682010531
        }
        """
        params = {
            'timeout': timeout
        }
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/hf/orders/dead-cancel-all', params=params)

    def query_hf_auto_cancel_setting(self):
        """
        https://docs.kucoin.com/spot-hf/#hf-auto-cancel-order-setting-query
        :return:
        {
            "timeout": 5,
            "symbols": "BTC-USDT",
            "currentTime": 1682010526,
            "triggerTime": 1682010531
        }
        """
        return self._request('GET', '/api/v1/hf/orders/dead-cancel-all/query')

    def get_hf_transaction_records(self, symbol, **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#hf-transaction-records
        :param symbol: Only returns order information for the specified trading pair
        :param kwargs:  Fill in parameters with reference documents
        :return:
        {
          "items":[
             {
                "id":2678765568,
                "symbol":"BTC-ETC",
                "tradeId":616179312641,
                "orderId":"6306cf6e27ecbe0001e1e03a",
                "counterOrderId":"6306cf4027ecbe0001e1df4d",
                "side":"buy",
                "liquidity":"taker",
                "forceTaker":false,
                "price":"1",
                "size":"1",
                "funds":"1",
                "fee":"0.00021",
                "feeRate":"0.00021",
                "feeCurrency":"USDT",
                "stop":"",
                "tradeType":"TRADE",
                "type":"limit",
                "createdAt":1661390702919
             }
          ],
          "lastId":2678765568
        }
        """
        params = {
            'symbol': symbol
        }
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/hf/fills', params=params)

    def create_oco_order(self, symbol, side, price, stopPrice, size, limitPrice, clientOid="", remark=None):
        """
        Place Order
        Do not include extra spaces in JSON strings in request body.
        Limitation
        The maximum untriggered stop orders for a single trading pair in one account is 20.
        https://www.kucoin.com/docs/rest/spot-trading/oco-order/place-order

        :param symbol: symbol, such as, ETH-BTC
        :param side: buy or sell
        :param price: Specify price for currency
        :param stopPrice: trigger price
        :param size: Specify quantity for currency
        :param limitPrice: The limit order price after take-profit and stop-loss are triggered
        :param clientOid: Client Order Id，unique identifier created by the user, the use of UUID is recommended, e.g. UUID, with a maximum length of 128 bits
        :param remark: Order placement remarks, length cannot exceed 100 characters (UTF-8)
        :return:
        {
             "orderId": "6572fdx65723280007deb5ex"
        }
        """
        params = {
            'symbol': symbol,
            'side': side,
            'price': price,
            'size': size,
            'stopPrice': stopPrice,
            'limitPrice': limitPrice,
            'tradeType': 'TRADE',
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        if remark:
            params['remark'] = remark

        return self._request('POST', '/api/v3/oco/order', params=params)

    def cancel_oco_order(self, orderId):
        """
        Cancel Order by orderId
        Request via this endpoint to cancel a single oco order previously placed.
        You will receive cancelledOrderIds field once the system has received the cancellation request. The cancellation request will be processed by the matching engine in sequence. To know if the request is processed (successfully or not), you may check the order status or the update message from the pushes.
        https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-orderid
        :param orderId: Path parameter, Order Id unique identifier
        :type: str
        :return:
        {
            "cancelledOrderIds": [ //List of two order IDs related to the canceled OCO order
                "vs9hqpbivnbpkfdj003qlxxx",
                "vs9hqpbivnbpkfdj003qlxxx"
            ]
        }
        """
        return self._request('DELETE', f'/api/v3/oco/order/{orderId}')

    def cancel_oco_order_by_clientOid(self, clientOid):
        """
        Cancel Order by clientOid
        https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-order-by-clientoid
        :param clientOid: Path parameter，Unique order id created by users to identify their orders
        :return:
        {
            "cancelledOrderIds": [ //List of two order IDs related to the canceled OCO order
                "vs9hqpbivnbpkfdj003qlxxx",
                "vs9hqpbivnbpkfdj003qlxxx"
            ]
        }
        """
        return self._request('DELETE', f'/api/v3/oco/client-order/{clientOid}')

    def cancel_all_oco_orders(self, symbol=None, orderIds=None):
        """
        Cancel Multiple Orders
        This interface can batch cancel OCO orders through orderIds.
        https://www.kucoin.com/docs/rest/spot-trading/oco-order/cancel-multiple-orders

        :param symbol: trading pair. If not passed, the oco orders of all symbols will be canceled by default.
        :param orderIds: Specify the order number, there can be multiple orders, separated by commas. If not passed, all oco orders will be canceled by default.
        :return:
        {
          "cancelledOrderIds": [
              "vs9hqpbivcq5dcu2003o19ta",
              "vs9hqpbivcq5dcu2003o19tb",
              "vs9hqpbive99kfdj003ql1j2",
              "vs9hqpbive99kfdj003ql1j3"
          ]
        }
        """
        params = {}
        if symbol:
            params['symbol']=symbol
        if orderIds:
            params['orderIds']=orderIds
        return self._request('DELETE', '/api/v3/oco/orders', params=params)

    def get_oco_order_by_orderId(self, orderId):
        """
        Get Order Info by orderId
        Request via this interface to get a oco order information via the order ID.
        https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-info-by-orderid
        :param orderId: Path parameter, Order Id unique identifier
        :return:
        {
          "orderId": "6572fdd65723280007deb5e0",
          "symbol": "FRM-USDT",
          "clientOid": "9a05f706a39eff673045b89foco1",
          "orderTime": 1702034902724,
          "status": "NEW"
        }
        """
        return self._request('GET', f'api/v3/oco/order/{orderId}')


    def get_oco_order_by_client_oid(self, clientOid):
        """
        Get Order Info by clientOid
        https://docs.kucoin.com/spot-hf/#obtain-details-of-a-single-hf-order-using-clientoid
        :param clientOid: Path parameter，Unique order id created by users to identify their orders
        :type: str
        :return:
        {
          "orderId": "6572fdd65723280007deb5e0",
          "symbol": "FRM-USDT",
          "clientOid": "9a05f706a39eff673045b89foco1",
          "orderTime": 1702034902724,
          "status": "NEW"
        }
        """
        return self._request('GET', f'/api/v3/oco/client-order/{clientOid}')

    def get_oco_orders(self,pageSize,currentPage,symbol=None,startAt=None,endAt=None,orderIds=None):
        """
        Get Order List
        Request via this endpoint to get your current OCO order list. Items are paginated and sorted to show the latest first. See the Pagination section for retrieving additional entries after the first page.
        https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-list
        :param pageSize: Size per page, minimum value 10, maximum value 500 (Mandatory)
        :param currentPage: Page number, minimum value 1 (Mandatory)
        :param symbol: Only order information for the specified Symbol is returned
        :param startAt: Start time (milliseconds)
        :param endAt: End time (milliseconds)
        :param orderIds: Specify orderId collection, up to 500 orders
        :return:
        {
          "currentPage": 1,
          "pageSize": 10,
          "totalNum": 4,
          "totalPage": 1,
          "items": [
              {
                  "orderId": "6572fdd65723280007deb5e0",
                  "symbol": "FRM-USDT",
                  "clientOid": "9a05f706a39eff673045b89foco1",
                  "orderTime": 1702034902724,
                  "status": "NEW"
              },
              {
                  "orderId": "6572fbbea24eca0007c8aaa9",
                  "symbol": "FRM-USDT",
                  "clientOid": "afe2d9deeba49f5ffee1792aoco1",
                  "orderTime": 1702034366305,
                  "status": "NEW"
              }
          ]
        }
        """
        params={
            'pageSize':pageSize,
            'currentPage':currentPage
        }
        if symbol:
            params['symbol']=symbol
        if startAt:
            params['startAt']=startAt
        if endAt:
            params['endAt']=endAt
        if orderIds:
            params['orderIds']=orderIds

        return self._request('GET', '/api/v3/oco/orders',params=params)

    def get_oco_order_details(self, orderId):
        """
        Get Order Details by orderId
        Request via this interface to get a oco order detail via the order ID.
        https://www.kucoin.com/docs/rest/spot-trading/oco-order/get-order-details-by-orderid
        :param orderId: Path parameter, Order Id unique identifier
        :type: str
        :return:
        {
            "orderId": "6572fdd65723280007deb5e0",
            "symbol": "FRM-USDT",
            "clientOid": "9a05f706a39eff673045b89foco1",
            "orderTime": 1702034902724,
            "status": "NEW",
            "orders": [
                {
                    "id": "vs9hqpbivnb5e8p8003ttdf1",
                    "symbol": "FRM-USDT",
                    "side": "sell",
                    "price": "1.00000000000000000000",
                    "stopPrice": "1.00000000000000000000",
                    "size": "25.00000000000000000000",
                    "status": "NEW"
                },
                {
                    "id": "vs9hqpbivnb5e8p8003ttdf2",
                    "symbol": "FRM-USDT",
                    "side": "sell",
                    "price": "3.00000000000000000000",
                    "stopPrice": "0.06000000000000000000",
                    "size": "25.00000000000000000000",
                    "status": "NEW"
                }
            ]
        }
        """
        return self._request('GET', f'api/v3/oco/order/details/{orderId}')

    def cancel_all_hf_orders(self):
        """
        Cancel all HF orders
        This endpoint can cancel all HF orders for all symbol.
        https://www.kucoin.com/docs/rest/spot-trading/spot-hf-trade-pro-account/cancel-all-hf-orders

        :return:
        {
          "succeedSymbols": [
            "BTC-USDT",
            "ETH-USDT"
          ],
          "failedSymbols": [
            {
                "symbol": "BTC-USDT",
                "error": "can't cancel, system timeout"
            }
          ],
        }
        """
        return self._request('DELETE', '/api/v1/hf/orders/cancelAll')
