from kucoin_futures.client import Trade

class MyTradeData(Trade):
    def create_bulk_order(self, orders, **kwargs):
        """
        Place bulk Orders
        """
        params = orders
        
        # if kwargs:
        #     params.update(kwargs)

        return self._request('POST', '/api/v1/orders/multi', params=params)
    
    def getOrderByOId(self, oid, **kwargs):
        """
        Get order by oid
        """
        
        # if kwargs:
        #     params.update(kwargs)

        return self._request('GET', '/api/v1/orders/byClientOid?clientOid='+oid)
    
    def getOpenStopOrderBySymbol(self, symbol, **kwargs):
        """
        https://docs.kumex.com/#get-untriggered-stop-order-list

        :param kwargs:c
        :return:
        {
      "currentPage": 1,
      "pageSize": 100,
      "totalNum": 1000,
      "totalPage": 10,
      "items": [
        {
            "id": "5cdfc138b21023a909e5ad55", //Order ID
            "symbol": "XBTUSDM",  //Ticker symbol of the contract
            "type": "limit",   //Order type, market order or limit order
            "side": "buy",  //Transaction side
            "price": "3600",  //Order price
            "size": 20000,  //Order quantity
            "value": "56.1167227833",  //Order value
            "dealValue": "0",  //Value of the executed orders
            "dealSize": 0,  //Executed order quantity
            "stp": "",  //Self trade prevention types
            "stop": "",  //Stop order type (stop limit or stop market)
            "stopPriceType": "",  //Trigger price type of stop orders
            "stopTriggered": false,  //Mark to show whether the stop order is triggered
            "stopPrice": null,  //Trigger price of stop orders
            "timeInForce": "GTC",  //Time in force policy type
            "postOnly": false,  //Mark of post only
            "hidden": false,  //Mark of the hidden order
            "iceberg": false,  //Mark of the iceberg order
            "visibleSize": null,  //Visible size of the iceberg order
            "leverage": "20",  //Leverage of the order
            "forceHold": false,  //A mark to forcely hold the funds for an order
            "closeOrder": false, //A mark to close the position
            "reduceOnly": false,  //A mark to reduce the position size only
            "clientOid": "5ce24c16b210233c36ee321d",  //Unique order id created by users to identify their orders
            "remark": null,  //Remark of the order
            "isActive": true,  //Mark of the active orders
            "cancelExist": false,  //Mark of the canceled orders
            "createdAt": 1558167872000  //Time the order created
            "settleCurrency": "XBT", //settlement currency
            "status": "open", //order status: “open” or “done”
            "updatedAt": 1558167872000 //last update time
        }
      ]
    }
        """
      

        return self._request('GET', '/api/v1/stopOrders?symbol='+symbol)
    def cancelOrderById(self, id):
        """
        Cancel Order by id
                "5cdfc120b21023a909e5ad52"
              ]
            }
          }
        """
        return self._request('DELETE', f'/api/v1/orders/{id}')
    def getMarkPrice(self, symbol):
        """
        Cancel Order by id
                "5cdfc120b21023a909e5ad52"
              ]
            }
          }
        """
        return self._request('GET', f'/api/v1/mark-price/{symbol}/current')
    def getContractDetails(self, symbol):
        """        
        :param symbol:  (Mandatory)
        :type: str
        :return:
        """
        return self._request('GET', f'/api/v1/contracts/{symbol}')
    def getAccountOverView(self, currency):
        """        
        :param currency:  (Mandatory)
        :type: str
        :return:
        """
        return self._request('GET', f'/api/v1/account-overview?currency={currency}')

    def getKlines(self, symbol, granularity,startTime=None, endTime=None):
        """        
        :param symbol:  (Mandatory)
        :type: str
        :param granularity:  (Mandatory)
        :type: int
        :param startTime:  
        :type: int
        :param stTime:  
        :type: int
        :return:
        """
        request = f'/api/v1/kline/query?symbol={symbol}&granularity={granularity}'
        if startTime is not None:
            request = request + f'&from={startTime}'
        if endTime is not None:
            request = request + f'&to={endTime}'

        return self._request('GET',request)
    
    def getAccountLedger(self, symbol, offset=0, forward=True, maxCount=10):
        """

        :param symbol: interest symbol (Mandatory)
        :type: str
        :param offset:  Start offset. The unique attribute of the last returned result of the last request. The data of (optional)
        the first page will be returned by default
        :type: int
        :param forward: his parameter functions to judge whether the lookup is forward or not (optional)
        :type: bool
        :param maxCount:Max record count (optional)
        :type : int
        :return:
          {
            "code": "200000",
            "data": {
              "hasMore": false, //Whether there are more pages
              "dataList": [
                {
                  "time": 1558596284040, //Event time
                  "type": "RealisedPNL", //Type
                  "amount": 0, //Transaction amount
                  "fee": null, //Fees
                  "accountEquity": 8060.7899305281, //Account equity
                  "status": "Pending", //Status. If you have held a position in the current 8-hour settlement period.
                  "remark": "XBTUSDM", //Ticker symbol of the contract
                  "offset": -1, //Offset
                  "currency": "XBT" //Currency
                },
                {
                  "time": 1557997200000,
                  "type": "RealisedPNL",
                  "amount": -0.000017105,
                  "fee": 0,
                  "accountEquity": 8060.7899305281,
                  "status": "Completed", //Status. Status. Funding period that has been settled.
                  "remark": "XBTUSDM",
                  "offset": 1,
                  "currency": "XBT"
                }
              ]
            }
          }
        """

        params = {'symbol': symbol}

        if offset:
            params['offset'] = offset
        if forward:
            params['forward'] = forward
        if maxCount:
            params['maxCount'] = maxCount
        return self._request('GET', '/api/v1/transaction-history', params=params)

