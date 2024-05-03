from typing import List
from myfuncs2 import logMessage, getUUIDBaseLong,updateBotOrder,updateBotGrid,updateBot, updateBotStatus
from myfuncs2 import LOG_INFO, LOG_DEBUG, LOG_WARN, LOG_ERROR
from structs import Fill,Bot,Order,GridItem, BotStatus
from datetime import datetime, date, timedelta
from myTradeData2 import MyTradeData

import json

ORDER_CANCELED      = 0
ORDER_OPEN          = 1
ORDER_COMPLETED     = 2
ORDER_PARTIALLY_FILLED = 3

FEE_RATE = 0.00020

#ORDER_TP_CREATED = 2
#ORDER_LIMIT_CREATED = 1
ORDER_WAITING = 0
ORDER_ACTIVE  = 3

class BotManager():
    def __init__(self, botData=None, botObject:Bot=None, myTrade:MyTradeData = None):
        self.gridItems:List[GridItem]  = []
        self.orders:List[Order] =[]
        if botObject is not None:
            self.bot = botObject   
        elif botData is not None:
            self.bot = Bot(botData)
            if "orders" in botData.keys():
                for order in botData["orders"]:
                    itemObj = Order(order=order)
                    self.orders.append(itemObj)

            if "gridItems" in botData.keys():
                for item in botData["gridItems"]:
                    itemObj = GridItem(gridItem=item)
                    self.gridItems.append(itemObj)

        self.TM  =  myTrade
        self.savePending = False  
        self.status:BotStatus = BotStatus()
    def orderExists(self, orderId):
        found = False
        for order in self.orders:
            if order.id == orderId:
                found = True
                break
        return found

    def addGridItemsList(self, gridItems=[]):
        for item in gridItems:
            itemObj = GridItem(gridItem=item)
            self.addGridItem(itemObj)

    def addGridItem(self, gridItem=GridItem):
        self.gridItems.append(gridItem)


    def addOrder(self,order:Order, saveOnFB=True):
        self.orders.append(order)
        if saveOnFB:
            updateBotOrder(botId=self.bot.id, orderId=order.id, record=order)
        self.status.orderCount     = self.status.orderCount + 1
        self.status.savePending    = True
        self.status.totalUpdatePending    = True
        if order.type == "limit" and order.clientOid != '':
            # LEnght ID  = 10 bot ID, 1 from separator _, 10 form grid itemid 
            #print(f'Updating order oid, {order.clientOid[:21]}')
            self.updateGridItemStatus(order.clientOid[:21], ORDER_OPEN)
        return
    
    def setEntryValueActivated(self):
        self.bot.entryValueActivated=True
        self.savePending = True
    
    def rebuildBotValues(self):
        self.status.fees       = 0
        self.status.sellOrders = 0
        self.status.buyOrders  = 0
        self.status.sellValue  = 0
        self.status.buyValue   = 0
        self.status.sellSize   = 0
        self.status.buySize    = 0
        self.status.realizedPNL= 0
        self.status.unRealizedPNL=0
        self.status.currentPositionMargin=0
        self.status.ordersMargin= 0
        self.status.realizedROE = 0
        self.status.totalROE    = 0
        self.status.totalPNL    = 0
        self.status.buyOrdersDetail   = []
        self.status.sellOrdersDetail  = []
        self.status.savePending = True
        self.status.totalUpdatePending= True

    def cancelOrder(self, order:Order):
        ret = False
        cancelledOrder = self.TM.cancelOrderById(order.orderId)
        if len(cancelledOrder['cancelledOrderIds']) > 0:
            self.updateOrderStatus(order,ORDER_CANCELED)
            ret = True
        return ret

    # def addFill(self, fill:Fill):
    #     self.totalUpdatePending = True
    #     self.savePending = True
    #     self.fills.append(fill)
    #     if fill.side == "buy":
    #         self.bot.buyValue   = self.bot.buyValue + fill.value
    #     else:
    #         self.bot.sellValue  = self.bot.sellValue + fill.value
    #     self.bot.fees = self.bot.fees + fill.fee
    #     self.bot.realizedPNL = (self.bot.sellValue - self.bot.buyValue) - self.bot.fees 
    
    def updateOrdersStatus(self, resetAllValues=False):
        #Clean all values
        if resetAllValues:
            self.rebuildBotValues()
        for order in self.orders:
            try:
                # order.filledSize  = 0
                # order.filledValue = 0
                if order.side == "buy":
                    a= "Debug point"
                    #print("Buy Order " + order.orderId)
                if resetAllValues:
                    order.filledSize =0
                    order.filledValue=0
                if order.status != ORDER_CANCELED and (resetAllValues or order.status != ORDER_COMPLETED):
                    orderServer = self.TM.get_order_details(order.orderId)
                    if orderServer["isActive"] and (resetAllValues or order.status != ORDER_OPEN):
                        self.updateOrderStatus(order,ORDER_OPEN, ignoreLogMessage=resetAllValues)
                    if orderServer["cancelExist"] and (resetAllValues or order.status != ORDER_CANCELED):
                        self.updateOrderStatus(order,ORDER_CANCELED, ignoreLogMessage=resetAllValues)
                    if orderServer["size"] == orderServer["filledSize"] and (resetAllValues or order.status != ORDER_COMPLETED):
                        self.updateOrderStatus(order,ORDER_COMPLETED, filledSize = orderServer["filledSize"] , filledValue= float(orderServer["filledValue"]), ignoreLogMessage=resetAllValues)
                    elif orderServer["filledSize"] != 0 :
                        self.updateOrderStatus(order,ORDER_PARTIALLY_FILLED, filledSize = orderServer["filledSize"] , filledValue=float(orderServer["filledValue"]) , ignoreLogMessage=resetAllValues)
            except Exception as e:
                logMessage(LOG_ERROR,f"Error getting order data on status update on bot. OrderID {order.orderId}\nError {str(e)}", bot=self.bot)
    
    def updateOrderStatus(self,order:Order,status, filledSize=0, filledValue=0, ignoreLogMessage=False):
        order.status     = status
        updateBotOrder(botId=self.bot.id, orderId=order.id, record=order)                
        #Not needed here, no change to BOT
        #self.savePending = True
        if status == ORDER_COMPLETED or status == ORDER_PARTIALLY_FILLED:  
            self.status.savePending = True
            self.status.totalUpdatePending = True
            prevFilled       = order.filledSize
            prevFilledValue  = order.filledValue
            order.filledSize = filledSize
            order.filledValue= filledValue
            if status == ORDER_PARTIALLY_FILLED:
                a =1 #Debug stop
            if order.side == "buy":
                if status == ORDER_COMPLETED:
                    self.status.buyOrders = self.status.buyOrders + 1
                self.status.buyValue   = self.status.buyValue  - prevFilledValue + order.filledValue
                self.status.buySize    = self.status.buySize   - prevFilled + (order.filledSize * self.bot.tickerMultiplier)
                self.status.buyOrdersDetail.append(order.id)
            else:
                if status == ORDER_COMPLETED:
                    self.status.sellOrders = self.status.sellOrders + 1
                self.status.sellValue  = self.status.sellValue - prevFilledValue + order.filledValue 
                self.status.sellSize   = self.status.sellSize - prevFilled + (order.filledSize * self.bot.tickerMultiplier)

                self.status.sellOrdersDetail.append(order.id)

            self.status.fees = (self.status.buyValue + self.status.sellValue) * FEE_RATE
            self.status.realizedPNL = (self.status.sellValue - self.status.buyValue) - self.status.fees 

        #Update status and filled size on server
        updateBotOrder(botId=self.bot.id, orderId=order.id, record=order)

        if order.clientOid != '':
            # Length ID  = 10 bot ID, 1 from separator _, 10 form grid itemid 
            #print(f'Updating order oid, {order.clientOid[:21]}, status {status}')
            self.updateGridItemStatus(order.clientOid[:21], status, ignoreLogMessage)
    
    def updateGridItemStatus(self,clientOid, status, ignoreLogMessage=False):
        for gridItem in self.gridItems:
            if gridItem.clientOid == clientOid:
                #Not needed here Grid is udpated on updateBotGrid below
                #self.savePending = True
                if status == ORDER_CANCELED or status == ORDER_COMPLETED :
                    gridItem.status = ORDER_WAITING
                    if not ignoreLogMessage:
                        if status == ORDER_CANCELED:
                            logMessage(LOG_INFO,f"Grid item reactivated due to order cancelation: price {gridItem.price}", bot=self.bot)
                        else:
                            logMessage(LOG_INFO,f"Grid item reactivated due to order completion: price {gridItem.price}", bot=self.bot)
                elif status == ORDER_OPEN:
                    if not ignoreLogMessage:
                        logMessage(LOG_INFO,f"Created limit order for grid item : price {gridItem.price}", bot=self.bot)
                    gridItem.status = ORDER_ACTIVE
                else:    
                    if not ignoreLogMessage:
                        logMessage(LOG_INFO,f"Grid item filled: price {gridItem.price}", bot=self.bot)
                    gridItem.status = ORDER_ACTIVE
                updateBotGrid(self.bot.id, gridId=gridItem.id, gridItem=gridItem)                
                break
                
    def updateFills(self):
        for order in self.orders:
            try:
                if order.status != ORDER_CANCELED and order.status != ORDER_COMPLETED:
                    orderServer = self.TM.get_order_details(order.orderId)
                    if orderServer["isActive"]:
                        self.updateOrderStatus(order,ORDER_OPEN)
                    if orderServer["cancelExist"]:
                        self.updateOrderStatus(order,ORDER_CANCELED)
                    if orderServer["size"] == orderServer["filledSize"]:
                        #self.updateOrderStatus(order,ORDER_COMPLETED)
                        self.updateOrderStatus(order,ORDER_COMPLETED, filledSize = orderServer["filledSize"] , filledValue= float(orderServer["filledValue"]))
                        # fills = self.TM.get_fills_details(orderId=order.orderId)
                        # for fillItem in fills['items']:
                        #     if not self.fillExists(tradeId=fillItem["tradeId"]):
                        #         x = Fill(symbol=fillItem["symbol"],orderId=fillItem["orderId"],tradeId=fillItem["tradeId"])
                        #         x.fromObject(fillItem)
                        #         self.addFill(x)
                    elif orderServer["filledSize"] != 0 :
                        self.updateOrderStatus(order,ORDER_PARTIALLY_FILLED, filledSize = orderServer["filledSize"] , filledValue=float(orderServer["filledValue"]) )
                        # fills = self.TM.get_fills_details(orderId=order.orderId)
                        # for fillItem in fills['items']:
                        #     if not self.fillExists(tradeId=fillItem["tradeId"]):
                        #         x = Fill(symbol=fillItem["symbol"],orderId=fillItem["orderId"],tradeId=fillItem["tradeId"])
                        #         x.fromObject(fillItem)
                        #     else:
                        #         print('exists')
                        #         self.addFill(x)
            except Exception as e:
                logMessage(LOG_ERROR,f"Error getting order data on fill update. OrderID {order.orderId}\nError {str(e)}", bot=self.bot)

    def updateResults(self, positionCalc=None, force = False):
        if force or self.status.totalUpdatePending:
            self.status.totalUpdatePending = False
            self.status.savePending = True
            if positionCalc is None:
                try:
                    position = self.TM.get_position_details(symbol= self.bot.symbol)
                    positionCalc=position
                    self.status.unRealizedPNL       =  position["unrealisedPnl"]+ position["realisedPnl"]
                    self.status.currentPositionMargin= position["currentCost"]
                    #This is negative (at least for sell)
                    #TODO: Check when implementing buy grid
                    self.status.currentPositionTotalCost  = position["posCost"]
                    self.status.currentPositionMarginCost  = position["posInit"]
                except Exception as e:
                    logMessage(LOG_ERROR,f"Error getting position on bot update {str(e)}", bot=self.bot)
            else:
                self.status.unRealizedPNL        = positionCalc["unrealisedPnl"] + positionCalc["realisedPnl"]
                self.status.currentPositionMargin= positionCalc["currentCost"]
                    #This is negative (at least for sell)
                    #TODO: Check when implementing buy grid
                self.status.currentPositionTotalCost  = positionCalc["posCost"]
                self.status.currentPositionMarginCost  = positionCalc["posInit"]

            #self.status.unRealizedPNL= 0
            self.status.availableMargin = self.bot.maxMargin
            try:
                self.status.ordersMargin = 0
                openOrders = self.TM.get_order_list(status="active",side=self.bot.side, symbol=self.bot.symbol)
                for item in openOrders['items']:
                    self.status.ordersMargin = self.status.ordersMargin + (float(item["value"])/float(item["leverage"]))
            except Exception as e:
                logMessage(LOG_ERROR,f"Error getting open orders on bot update {str(e)}", bot=self.bot)

            # if position["currentQty"] > 0:
            #     self.bot.buyValue = self.bot.buyValue   - position["posCost"] 
            # else:
            #     self.bot.sellValue = self.bot.sellValue + position["posCost"] 
            if (self.status.sellSize - self.status.buySize + (position["currentQty"] * self.bot.tickerMultiplier)) != 0:
                logMessage(LOG_WARN,f"Unbalanced orders, updating ROE data on next cycle", bot=self.bot)
            else:
                self.status.realizedPNL = (self.status.sellValue - self.status.buyValue) - self.status.fees + self.status.currentPositionTotalCost
                self.status.ordersMargin = round(self.status.ordersMargin,2)
                self.status.availableMargin = round(self.status.availableMargin - self.status.currentPositionMarginCost - self.status.ordersMargin,2)
                if self.bot.addPNLToMarginAvailable:
                    self.status.availableMargin = round(self.status.availableMargin+self.status.realizedPNL,2)

                self.status.realizedROE=((self.bot.maxMargin+self.status.realizedPNL) / self.bot.maxMargin)-1
                self.status.totalROE= ((self.bot.maxMargin+self.status.realizedPNL+self.status.unRealizedPNL) / self.bot.maxMargin)-1
                self.status.totalPNL=self.status.unRealizedPNL+self.status.realizedPNL
            self.status.statusPosition =  json.dumps(positionCalc)
        return
    def checkPendingSaves(self):
        if self.savePending:
            try:
                updateBot(self.bot)
                self.savePending = False
            except Exception as e:
                logMessage(LOG_ERROR,f"Error updating bot on FB: { str(e) }", bot=self.bot)

        if self.status.savePending:
            if self.status.totalUpdatePending:
                self.updateResults()
            try:
                updateBotStatus(self.bot.id,self.status)
                self.status.savePending = False
            except Exception as e:
                logMessage(LOG_ERROR,f"Error updating bot status on FB: { str(e) }", bot=self.bot)

#     def tmpRefactor(self):
#         self.fills = []
#         self.orderCount = 0
#         self.fees       = 0
#         self.sellOrders = 0
#         self.buyOrders  = 0
#         self.sellValue  = 0
#         self.buyValue   = 0
#         self.sellSize   = 0
#         self.buySize    = 0
#         self.realizedPNL= 0
#         self.unRealizedPNL=0
#         self.currentPositionMargin=0
#         self.ordersMargin=0
#         self.realizedROE =0
#         self.totalROE    =0
#         self.totalPNL    =0
#         for item in self.gridItems:
#            found = False
#            #Orders in GridItems
#            for gridOrder in item.orders:
#                 for order in self.orders:
#                     if order.orderId == gridOrder["orderId"]:
#                         found = True
#                         break
#                 #Add order to bot root
#                 if not found:
#                     x = Order(clientOid=item.clientOid)
#                     x.fromObject(gridOrder)
#                     self.addOrder(x)

#         for adjustedOrder in self.adjustedOrders:
#             found = False
#             #Orders in adjustedOrders
#             for order in self.orders:
#                 if order.orderId == adjustedOrder.orderId:
#                     found = True
#                     break
#                 #Add order to bot root
#             if not found:
#                self.addOrder(adjustedOrder)

#         allOrders24Hrs = self.TM.getRecentDoneOrders(self.symbol)
#         for xOrder in allOrders24Hrs:
#             if xOrder['clientOid'][:10] == self.id:
#                 for order in self.orders:
#                     if order.orderId == xOrder["clientOid"]:
#                         found = True
#                         break
#                 #Add order to bot root
#                 if not found:
#                     x = Order(clientOid=xOrder['clientOid'], orderId=xOrder['id'], type= "TP" if xOrder['reduceOnly'] else "limit", side=xOrder['side'], reduceOnly=xOrder['reduceOnly'])
# #                    x.fromObject(xOrder)
#                     self.addOrder(x)

#         count = 0
#         for order in self.orders:
#             count = count +1
#             orderServer = self.TM.get_order_details(order.orderId)
#             order.side       = orderServer["side"]
#             order.reduceOnly = orderServer["reduceOnly"]
#             order.clientOid  = orderServer["clientOid"]

#             if orderServer["isActive"]:
#                 self.updateOrderStatus(order,ORDER_OPEN)
#             if orderServer["cancelExist"]:
#                 self.updateOrderStatus(order,ORDER_CANCELED)
#             if orderServer["size"] == orderServer["filledSize"]:
#                 self.updateOrderStatus(order,ORDER_COMPLETED, filledSize = orderServer["filledSize"] , filledValue=float(orderServer["filledValue"]) )
#             elif orderServer["filledSize"] != 0 :
#                 self.updateOrderStatus(order,ORDER_PARTIALLY_FILLED, filledSize = orderServer["filledSize"] , filledValue=float(orderServer["filledValue"]) )
#             order.msg = 'Adjusted'
#             # if order.status != ORDER_CANCELED:
#             #     fills = self.TM.get_fills_details(orderId=order.orderId)
#             #     for fillItem in fills['items']:
#             #         x = Fill(symbol=fillItem["symbol"],orderId=fillItem["orderId"],tradeId=fillItem["tradeId"])
#             #         x.fromObject(fillItem)
#             #         self.addFill(x)
#             # else:
#             #     fills = self.TM.get_fills_details(orderId=order.orderId)
#             #     if len(fills[ 'items']) > 0:
#             #         print('cancelled is filled!!!!!')
#             print(f'orderId { order.orderId}, {order.side}, {order.status}, { order.clientOid}, {order.reduceOnly}, {order.filledSize}, { order.filledValue}' )

#         self.updateResults()
#         # new_list = sorted(self.fills, key=lambda x: x.tradeTime)
#         # total = 0
#         # for x in new_list:
#         #     if x.side == "sell":
#         #         total = total - x.size
#         #         print(f'Total: {total}, SELL-> Size: = -{x.size}, tradeId : {x.tradeId}, tradeId : {x.orderId}')
#         #     elif x.side == "buy":
#         #         total = total + x.size
#         #         print(f'Total: {total}, BUY -> Size: =  {x.size}, tradeId : {x.tradeId}, tradeId : {x.orderId}')
    
        

#         a=1
    




