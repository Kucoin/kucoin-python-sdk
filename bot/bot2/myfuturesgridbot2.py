import json
import asyncio
from typing import List
from kucoin.client import User
from myTradeData2 import MyTradeData
from secrets_API_KEYS import API_KEY,API_SECRET,passphrase
from datetime import datetime, date, timedelta
from myfuncs2 import date_to_milliseconds, current_milli_time, deleteOrders, getOldBot, logMessage, getUUIDBaseLong,updateBot,updateBotGrid,getMyBots,updateBotOrder,getGridItems,getOrders,getRecord, getStatus,updateAccountStatus,getBotsToUpdate
from myfuncs2 import LOG_INFO, LOG_DEBUG, LOG_WARN, LOG_ERROR,LOG_ALWAYS

from botClass import BotManager,ORDER_CANCELED,ORDER_OPEN, ORDER_PARTIALLY_FILLED, ORDER_COMPLETED
from structs import Bot, Order, GridItem,BotStatus

ORDER_TP_CREATED = 2
ORDER_LIMIT_CREATED = 1
ORDER_WAITING = 0

DEACTIVATE_BOT_IMEDIATELY = 1
DEACTIVATE_BOT_AFTER_CLOSE_POSITION = 2

def getStepvalue(price:float, bot:Bot):
  if bot.stepPercentage != 0:
    step = (price * (bot.stepPercentage/100)) /float(bot.leverage)
  else:
    step = bot.step
  
  return step


def createStopOrders(botManager: BotManager, bot:Bot, position):
  try:
    stopOrders= {"items":[]}
    openStopOrders= {"items":[]}
    # Get Filled stop orders
    try:
      filledStopOrders = botManager.TM.get_order_list(status="active",side="buy" if position['currentQty'] < 0 else "sell", symbol=bot.symbol)
      for stopOrderTmp in filledStopOrders["items"]:
        if stopOrderTmp["reduceOnly"]:
          stopOrders["items"].append(stopOrderTmp)
    except Exception as e:
      logMessage(LOG_ERROR,f'Error getting TP Active order list:: {str(e)}', bot)
    # Get OPEN stop orders
    try:
      openStopOrders =  botManager.TM.getOpenStopOrderBySymbol(bot.symbol)
    except Exception as e:
      logMessage(LOG_ERROR,f'Error getting TP OPEN order list:: {str(e)}', bot)    
    for stop in stopOrders["items"]:
      if not botManager.orderExists(stop['id']):
        orderCreatedOnFillStop = Order(orderId = stop['id'], clientOid="", type="TP", status= ORDER_OPEN, msg = "created OnFillStop", side = stop["side"], price = float(stop["price"]),reduceOnly=stop["reduceOnly"])
        botManager.addOrder(orderCreatedOnFillStop)
        logMessage(LOG_WARN, 'Stop Order added from server', bot)
    stopOrders["items"]= stopOrders["items"] + openStopOrders["items"]
    step = getStepvalue(position['avgEntryPrice'],bot)
    if position['id'] != '':
      createStopOrder = False
      ordersToCancel = []
      signal = ( -1 if position['currentQty'] < 0 else 1)

      if len(stopOrders['items']) == 0:
        createStopOrder = True
      else:

        for order in stopOrders['items']:
          if order['reduceOnly']:
            #If there is already one order in the list to be canceled, cancel all
            if len(ordersToCancel)>0:
              message = 'Canceling to redefine stop orders'
              ordersToCancel.append([order['id'], message])
            else:
              price = float(order['stopPrice'] if order['stopPrice'] is not None else order['price'])
              message = order['id']
              #Check if current stop order size is less than position  
              if (order['size']) < (abs(position['currentQty'])) :
                message = message+f'TP size is lower than position, canceling and creating new TP, size {order["size"]}, position size {abs(position["currentQty"])}\n'
                createStopOrder = True            
              #Check if current stop order is above or below than average entry price  
              if  not createStopOrder and (signal < 0 and price > round(position['avgEntryPrice'],bot.tickerRound)) or \
                                          (signal > 0 and price < round(position['avgEntryPrice'],bot.tickerRound)) :
                message = message+f'TP price is above/below average price, position price {position["avgEntryPrice"]}, TP stop price {order["price"]}, new TP stop price {position["avgEntryPrice"] - step}'
                createStopOrder = True              
              #Check if current stop order is above or below expected step regarding average entry price  
              if not createStopOrder and  (signal < 0 and price < round(position['avgEntryPrice']-step ,bot.tickerRound)) or \
                                          (signal > 0 and price > round(position['avgEntryPrice']+step ,bot.tickerRound)) :
                message = message+f'TP price is more than one step away, canceling and creating new TP, position price {position["avgEntryPrice"]}, TP stop price {order["price"]}, new TP stop price {position["avgEntryPrice"] - step}'
                createStopOrder = True

              if createStopOrder:   
                ordersToCancel.append([order['id'], message])
                # stopOrder =   {
                #         "clientOid": order["clientOid"],
                #         "side": order['side'],
                #         "symbol": order['symbol'],
                #         "type":"limit",
                #         "size": str(position['currentQty'] * -1) if position['currentQty'] < 0 else str(position['currentQty']),
                #         "leverage": order['leverage'],
                #         "stop": "up" if order['side'] == "buy" else "down",
                #         "price": round((position['avgEntryPrice'] + (step*signal)),bot.tickerRound),
                #         "stopPrice": round((position['avgEntryPrice'] + (step*signal)),bot.tickerRound),
                #         "stopPriceType": "TP",
                #         "reduceOnly": True
                #       }
                # try:                
                #   if not botManager.cancelOrder(Order(orderId=order['id'])):
                #     message = f'Failed to cancel order, orderId{order["id"]}'
                #   else:
                #     orderCreationReturn = botManager.TM.createOrder(stopOrder)  
                #     if not orderCreationReturn['orderId'] is None and orderCreationReturn['orderId'] != '':
                #       orderCreated = Order(orderId = orderCreationReturn['orderId'], clientOid=order["clientOid"], type="TP", status= ORDER_OPEN, msg = "created", side = stopOrder["side"], price = float(stopOrder["price"]),reduceOnly=True)
                #       botManager.addOrder(orderCreated)
                #       details = f'Stop Order Price: {price}\nAvg Entry Price:{round(position["avgEntryPrice"],bot.tickerRound)}\n'
                #       details = details + f'Order TP Size:{order["size"]}\nPosition Size {((position["currentQty"]) * -1) if position["currentQty"] < 0 else (position["currentQty"]) }'
                #       message = f'Adjusted TP - size:{stopOrder["size"]} - price:{stopOrder["price"]}\n'+details
                #       logMessage(LOG_INFO,message,bot=bot)
                #     else:
                #       error = f'Error adjusting TP - size:{stopOrder["size"]}, price:{stopOrder["price"]}, message: {orderCreationReturn["msg"]}'
                #       logMessage(LOG_ERROR,error)
                # except Exception as e:
                #   error = 'Error adjusting TP::  '+str(e)
                #   logMessage(LOG_ERROR,error,bot.symbol)

      for orderToCancel in ordersToCancel:
        message = f'Canceling TP order, orderId {orderToCancel[0]}, msg: {orderToCancel[1]}'
        logMessage(LOG_INFO,message, bot)
        if not botManager.cancelOrder(Order(orderId=orderToCancel[0],msg=orderToCancel[1])):
          error = f'Failed to cancel order, orderId {order["id"]}'
          logMessage(LOG_WARN,error, bot)
      
      if createStopOrder:
        type = "limit"
        price = round(position['avgEntryPrice'] + (step*signal), bot.tickerRound)
        if (signal == -1 and position['markPrice'] < price) or \
            (signal == 1 and position['markPrice'] > price) :
          type = "market"
        stopOrder =   {
                "clientOid": bot.id+"_"+getUUIDBaseLong()+"_TP",
                "side": "buy" if position['currentQty'] < 0 else "sell",
                "symbol": position['symbol'],
                "type":type,
                "size": str(position['currentQty'] * -1) if position['currentQty'] < 0 else str(position['currentQty']),
                "leverage": str(position['realLeverage']),
                "price": price,
                # "stop": "down" if position['currentQty'] < 0 else "up",
                # "stopPrice": round(position['avgEntryPrice'] + (step*signal), bot.tickerRound),
                # "stopPriceType": "TP",
                "reduceOnly": True
              }
        try:
          orderCreationReturn = botManager.TM.createOrder(stopOrder)  
          if not orderCreationReturn['orderId'] is None and orderCreationReturn['orderId'] != '':
            orderAdded = False
            while not orderAdded:  
              try:
                orderCreated = Order(orderId = orderCreationReturn['orderId'], clientOid=stopOrder["clientOid"], type="TP", status= ORDER_OPEN, msg = "created", side = stopOrder["side"], price = float(stopOrder["price"]),reduceOnly=True)
                botManager.addOrder(orderCreated)
                orderAdded = True
                logMessage(LOG_INFO,"Created TP Order for position", bot)

              except Exception as e:
                logMessage(LOG_ERROR,f'Error adding TP TO BOT LIST - clientOid: {stopOrder["clientOid"]}, size:{stopOrder["size"]}, price:{stopOrder["price"]}, orderId: {orderCreationReturn["orderId"]} -', bot)
                asyncio.sleep(1)
          else:
            error = f'Error creating TP - clientOid: {stopOrder["clientOid"]}, size:{stopOrder["size"]}, price:{stopOrder["price"]}, message: {orderCreationReturn["msg"]}'
            logMessage(LOG_ERROR,error, bot)

        except Exception as e:
          error = 'Error setting adjusted TP::  '+str(e)
          logMessage(LOG_ERROR,error, bot)
    else:
      if botManager.status.prevROEPcnt != 0: 
        message = f'Position symbol [{bot.symbol}] closed, last known ROE: { round(botManager.status.prevROEPcnt*100,2)}%'
        logMessage(LOG_INFO,message, bot)
        botManager.status.prevROEPcnt = 0
  except Exception as e:
    error = 'Error checking stop orders:  '+str(e)
    logMessage(LOG_ERROR,error, bot)

def addManualOrdersToBot(botManager: BotManager, bot:Bot):
    try:
      orders = botManager.TM.get_order_list(status="active",symbol=bot.symbol)
      for order in orders["items"]:
        #Is manual order
        if order["clientOid"] == '':
          if not botManager.orderExists(order['id']):
            try: 
              #TODO: Adicionar controle aqui para garantizar que seja criada a ordem (se cancelar e nao criar fica pendente e nunca mais vai adicionar)
              if not botManager.cancelOrder(Order(orderId=order['id'],msg="Cancelling order added manually")):
                error = f'Failed to cancel manually added order, orderId {order["id"]}'
                logMessage(LOG_WARN,error,bot.symbol)
              else:
                try:
                  orderReduceOnly = order["reduceOnly"]
                  order["clientOid"] = bot.id+"_"+getUUIDBaseLong()+"_TP" if orderReduceOnly else ""
                  orderCreationReturn = botManager.TM.createOrder(order)  
                  if not orderCreationReturn['orderId'] is None and orderCreationReturn['orderId'] != '':
                    orderAdded = False
                    while not orderAdded:
                      try:
                        orderCreated = Order(orderId = orderCreationReturn['orderId'], clientOid=order["clientOid"], type="TP"  if order["side"] != bot.side else order['type'], status= ORDER_OPEN, msg = "created", side = order["side"], price = float(order["price"]),reduceOnly=order["reduceOnly"])
                        botManager.addOrder(orderCreated)
                        orderAdded = True
                        logMessage(LOG_INFO,"Created substitute to manually added order", bot)
                      except Exception as e:
                        logMessage(LOG_ERROR,f'Error adding substitute order TO BOT LIST - clientOid: {order["clientOid"]}, size:{order["size"]}, price:{order["price"]}, orderId: {orderCreationReturn["orderId"]} -', bot)
                        asyncio.sleep(1)
                  else:
                    error = f'Error creating substitute order - size:{order["size"]}, price:{order["price"]}, message: {orderCreationReturn["msg"]}'
                    logMessage(LOG_ERROR,error, bot)
                except Exception as e:
                  logMessage(LOG_ERROR,f'Error creating substitute to manually added order: {str(e)}', bot)
              
            except Exception as e:
              logMessage(LOG_ERROR,f'Error canceling manually added order: {str(e)}', bot)

    except Exception as e:
      logMessage(LOG_ERROR,f'Error getting TP Active order list:: {str(e)}', bot)

def copyBotParams(myTrade:MyTradeData):
  
  
  bot = getRecord('cryptoBot', '000000Kd1G')
  newBotToDeactivate = BotManager(botData=bot, myTrade=myTrade)
  newBotToDeactivate.bot.active= False
  updateBot(newBotToDeactivate.bot)

  bot["id"]     = getUUIDBaseLong()
  bot["date"]   = datetime.utcnow().isoformat()
  bot['dateMiliSeconds']= date_to_milliseconds(bot["date"])
  bot["active"] = True
  newBot = BotManager(botData=bot, myTrade=myTrade)
  updateBot(newBot.bot)

  bot = getRecord('cryptoBot', '000000IQ4N')
  newBotToDeactivate = BotManager(botData=bot, myTrade=myTrade)
  newBotToDeactivate.bot.active= False
  updateBot(newBotToDeactivate.bot)

  bot["id"]     = getUUIDBaseLong()
  bot["date"]   = datetime.utcnow().isoformat()
  bot['dateMiliSeconds']= date_to_milliseconds(bot["date"])
  bot["active"] = False
  newBot = BotManager(botData=bot, myTrade=myTrade)
  updateBot(newBot.bot)


  bot = getRecord('cryptoBot', '000000Kd1I')
  newBotToDeactivate = BotManager(botData=bot, myTrade=myTrade)
  newBotToDeactivate.bot.active= False
  updateBot(newBotToDeactivate.bot)

  bot["id"]     = getUUIDBaseLong()
  bot["date"]   = datetime.utcnow().isoformat()
  bot['dateMiliSeconds']= date_to_milliseconds(bot["date"])
  bot["active"] = False
  newBot = BotManager(botData=bot, myTrade=myTrade)
  updateBot(newBot.bot)

  updateBot(newBot.bot)
def copyBotParamsFromOld(myTrade:MyTradeData):
  
  bot = getOldBot(code= '000000IqjT')
  bot[0]["id"]     = getUUIDBaseLong()
  bot[0]["date"]   = datetime.utcnow().isoformat(), 
  bot[0]["active"] = False
  newBot = BotManager(botData=bot[0], myTrade=myTrade)
  
  updateBot(newBot.bot)



def migrateBot(myTrade:MyTradeData):
  botsFromDB = getMyBots()

  for bot in botsFromDB:
    bot["id"]     = getUUIDBaseLong()
    bot["date"]   = datetime.utcnow().isoformat(), 
    bot["active"] = False
    newBot = BotManager(botData=bot, myTrade=myTrade)
    
    updateBot(newBot.bot)

    for item in newBot.gridItems:
        updateBotGrid(newBot.bot.id,item.id,item)
    for order in newBot.orders:
        updateBotOrder(newBot.bot.id,order.id,order)

def checkMissedOrders(botManager:BotManager):
    (addedOrders,lastStartedAt) = getMissedOrders(botManager)
    if len(addedOrders) > 0:
      for order in addedOrders:
          botManager.orders.append(order)
          updateBotOrder(botManager.bot.id,order.id,order)
          message = f"Added missing order {order.id }"
          logMessage(LOG_WARN,message, bot=botManager.bot, log_level=LOG_DEBUG)
      botManager.status.lastOrderCheck = lastStartedAt
      botManager.status.savePending = True
      botManager.checkPendingSaves()

    return len(addedOrders)>0
def initializeBot(botManager:BotManager):
    logMessage(LOG_INFO,"Creating grid items for first time",bot=botManager.bot)
    tickerDef = False
    while not tickerDef:
      try:
        contractInfo = botManager.TM.getContractDetails(botManager.bot.symbol)
        tickerDef    = True
      except Exception as e:
          error = 'Error getting ticker::  '+str(e)
          logMessage(LOG_ERROR,error,bot=botManager.bot)
    tickerDec = contractInfo['tickSize']
    tickerRound =0
    while tickerDec <1:
      tickerDec   = tickerDec * 10
      tickerRound = tickerRound + 1
    botManager.bot.tickerRound = tickerRound
    tickerMult = contractInfo['multiplier']
    botManager.bot.tickerMultiplier = tickerMult

    tickerMultRound =0
    while tickerMult <1:
      tickerMult   = tickerDec * 10
      tickerMultRound = tickerMultRound + 1
    if tickerMultRound > 0:
      tickerMultRound = tickerMultRound - 1
    botManager.bot.tickerMultiplierRound = tickerMultRound
    price = botManager.bot.start
    updateBot(botManager.bot)
    grids = 1000
    for i in range(1,grids):
      id = botManager.bot.id + "_"+ getUUIDBaseLong(i)
      step = getStepvalue(price,botManager.bot)
      if price <= botManager.bot.end:
        gridItem = {
          "clientOid":id,
          "id": id,
          "side":"sell",
          "symbol":botManager.bot.symbol,
          "type":"limit",
          "price": str(round(price,botManager.bot.tickerRound)),
          "size": str(botManager.bot.size),
          "leverage": botManager.bot.leverage,
          "status" : ORDER_WAITING,
          "step": step,
        }
        gridItemObj =GridItem(gridItem)
        botManager.addGridItem(gridItemObj)
        updateBotGrid(botId=botManager.bot.id, gridId=gridItemObj.id, gridItem=gridItemObj)
      else:
        break
      price = price + step
def getBots(myTrade:MyTradeData):

  botsFromDB = getMyBots()
  bots: List[BotManager] = []

  for bot in botsFromDB:
    if False:
      bot["id"]     = getUUIDBaseLong()
      bot["date"]   = datetime.utcnow().isoformat() 
      #bot["orders"] = 
    if "dateMiliSeconds" not in bot.keys():
        bot['dateMiliSeconds']= date_to_milliseconds(bot["date"][0])
    newBot = BotManager(botData=bot, myTrade=myTrade)
    #newBot = BotManager(bot, myTrade)
    bots.append(newBot)
  
  for botManager in bots:
    #botManager.bot.stepPercentage = 8
    gridList = getGridItems(botManager.bot.id)
    #This does not updates Database
    botManager.addGridItemsList(gridList)  
    orderList = getOrders(botManager.bot.id)    

    for item in orderList:
         itemObj = Order(order=item)
         botManager.orders.append(itemObj)

    currStatus = getStatus(botManager.bot.id)
    if currStatus is not None:
      botManager.status = BotStatus(currStatus)

    if botManager.status.lastOrderCheck == 0:
      botManager.status.lastOrderCheck = botManager.bot.dateMiliSeconds

    checkMissedOrders(botManager)
    if len(botManager.gridItems) == 0:
      #This saves new data to BOT, and saves new Grid Items
      initializeBot(botManager)
      
  return bots

def releaseOrdersMargin(botManager:BotManager, bot:Bot):
  currPrice = 0
  #Cheks order status on server
  botManager.updateOrdersStatus()
  for order in botManager.orders:
    if not order.reduceOnly:
      #Check if order needs to be closed to release order margin (over maximum or below minimum steps)
      if order.status == ORDER_OPEN:
        try:
          if currPrice ==0:
            currPrice = botManager.TM.getMarkPrice(bot.symbol)['value']
          if order.side == 'sell':
              # close orders over  four grids up
              step = getStepvalue(order.price,bot)
              if float(order.price)  >  currPrice + ((bot.maxGridSteps+ 1 + 1/10) * step):
                try:
                  if botManager.cancelOrder(order):
                    message = f'Canceled over limit order => Order price: {order.price}, current price {currPrice}'
                    logMessage(LOG_INFO,message,bot=bot)
                  else:
                    message = f'Canceled over limit order failed => Order price: {order.price}, current price {currPrice}'
                    logMessage(LOG_WARN,message,bot=bot)
                except Exception as e:
                  error = 'Error canceling over limit order::  '+str(e)
                  logMessage(LOG_ERROR,error,bot=bot)
          else:
            # close orders below four grids down
            if float(order.price)  <  currPrice - ((bot.maxGridSteps+ 1 + 1/10) * step):
              try:
                if botManager.cancelOrder(order):
                  message = f'Canceled below limit order => Order price: {order.price}, current price {currPrice}'
                  logMessage(LOG_INFO,message,bot=bot)
                else:
                  message = f'Canceled over limit order failed => Order price: {order.price}, current price {currPrice}'
                  logMessage(LOG_WARN,message,bot=bot)
              except Exception as e:
                error = 'Error canceling below limit order::  '+str(e)
                logMessage(LOG_ERROR,error,bot=bot)
        except Exception as e:
          error = 'Error getting current price::  '+str(e)
          logMessage(LOG_ERROR,error,bot=bot)



def createLimitOrders(botManager:BotManager, bot:Bot,accountBalance,startTime, position):
  currPrice = 0
  if position["posInit"] > bot.maxMargin:
    #TODO: Set Bot to sleep
    a=1
  else:
    for gridItem  in botManager.gridItems:
      #Create orders
      if gridItem.status == ORDER_WAITING:
        try:
          if currPrice ==0:
            currPrice = botManager.TM.getMarkPrice(bot.symbol)['value']
            try:             
              kLines = botManager.TM.getKlines(bot.symbol,1,startTime)
              length = len(kLines)
              minimum = kLines[length-1][3]
              maximum = kLines[length-1][2]
              startTime = current_milli_time()
            except:
              minimum = currPrice
              maximum = currPrice
          if True or bot.status.availableMargin > (float(gridItem.price)/float(bot.leverage))*(float(gridItem.size)/float(bot.leverage)):
            if bot.side == 'sell':
              if bot.entryValueActivated or maximum >= bot.entryValue:
                if not bot.entryValueActivated:
                  botManager.setEntryValueActivated()
                # only open up to four grids up
                if float(gridItem.price)  <  currPrice + ((bot.maxGridSteps+ 1/10) * gridItem.step):
                  if minimum < float(gridItem.price) - gridItem.step:
                    if bot.increaseSizeByROE is not None and  bot.increaseSizeByROE and botManager.status.realizedROE > 0 :
                      # Protection against bad calculated ROE
                      if botManager.status.realizedROE < 1:
                        if bot.tickerMultiplierRound == 0:
                          size = str(int(round(float(gridItem.size) * (1+botManager.status.realizedROE),bot.tickerMultiplierRound)))
                        else:
                          size =  str(round(float(gridItem.size) * (1+botManager.status.realizedROE),bot.tickerMultiplierRound))
                      else:
                        size =  gridItem.size
                    else:
                      size =  gridItem.size
                    #TODO: AdjustSize by ticker multiplier
                    gridItem.lastOpenSize = size
                    limitOrder =   {
                      "clientOid": gridItem.clientOid+"_"+getUUIDBaseLong(lengthID=5),
                      "side": bot.side,
                      "symbol": bot.symbol,
                      "type":"limit",
                      "size": size,
                      "leverage": bot.leverage,
                      "price": gridItem.price
                    }
                    try:
                      orderCreationReturn = botManager.TM.createOrder(limitOrder)  
                      if not orderCreationReturn['orderId'] is None:
                        orderAdded = False
                        while not orderAdded:
                          try:
                            orderCreated = Order(orderId = orderCreationReturn['orderId'], clientOid=limitOrder["clientOid"],type="limit", status= ORDER_OPEN, msg = "created", side = bot.side, price = float(limitOrder["price"]))
                            botManager.addOrder(orderCreated)
                            orderAdded = True
                            message = f'Order created - minimum: {minimum}, price: {limitOrder["price"]}'
                            logMessage(LOG_INFO,message,bot=bot)
                          except Exception as e:
                            logMessage(LOG_ERROR,f'Error adding limit order TO BOT LIST - clientOid: {limitOrder["clientOid"]}, size:{limitOrder["size"]}, price:{limitOrder["price"]}, orderId: {orderCreationReturn["orderId"]} -', bot)
                            asyncio.sleep(1)
                        #print(b)
                      else:
                        if orderCreationReturn['code'] == '300018':
                          message = f'Error creating limit order - minimum: {minimum}, price: {limitOrder["price"]}, orderOid: {gridItem.clientOid},  message: {orderCreationReturn["msg"]}\nChanging order status'
                          #changegridItemStatus(clientOId=order['clientOid'],status=ORDER_LIMIT_CREATED, bot=bot)
                          logMessage(LOG_WARN,message,bot=bot)
                        else:
                          message = f'Error creating limit order - minimum: {minimum}, price: {limitOrder["price"]}, message: {orderCreationReturn["msg"]}'
                        logMessage(LOG_ERROR,message,bot=bot)
                    except Exception as e:
                      error = f'Error creating limit order - minimum: {minimum}, price: {limitOrder["price"]}, message: {str(e)}'
                      logMessage(LOG_ERROR,error,bot=bot)

            else:
              if bot.entryValueActivated or minimum <= bot.entryValue:
                if not bot.entryValueActivated:
                  botManager.setEntryValueActivated()
                # only open up to four grids down
                if float(gridItem.price)  >  currPrice - ((bot.maxGridSteps+ 1/10) *  gridItem.step):
                  if maximum > float(gridItem.price) +  gridItem.step:
                    if bot.increaseSizeByROE is not None and  bot.increaseSizeByROE and botManager.status.realizedROE >0 :
                      # Protection against bad calculated ROE
                      if botManager.status.realizedROE < 1:
                        if bot.tickerMultiplierRound == 0:
                          size = str(int(round(float(gridItem.size) * (1+botManager.status.realizedROE),bot.tickerMultiplierRound)))
                        else:
                          size =  str(round(float(gridItem.size) * (1+botManager.status.realizedROE),bot.tickerMultiplierRound))
                      else:
                        size =  gridItem.size
                    else:
                      size =  gridItem.size
                    gridItem.lastOpenSize = size
                    limitOrder =   {
                      "clientOid":gridItem.clientOid,
                      "side": bot.side,
                      "symbol": bot.symbol,
                      "type":"limit",
                      "size": size,
                      "leverage": bot.leverage,
                      "price": gridItem.price
                    }               
                    try:   
                      orderCreationReturn = botManager.createOrder(limitOrder)  
                      if not orderCreationReturn['orderId'] is None:
                        orderAdded = False
                        while not orderAdded:
                          try:
                            orderCreated = Order(orderId = orderCreationReturn['orderId'], clientOid=limitOrder["clientOid"], type="limit", status= ORDER_OPEN, msg = "created", side = bot.side, price = float(limitOrder["price"]))
                            botManager.addOrder(orderCreated)
                            orderAdded = True
                            message = f'Order created - maximum: {maximum}, price: {limitOrder["price"]}'
                            logMessage(LOG_INFO,message,bot=bot)
                          except Exception as e:
                            logMessage(LOG_ERROR,f'Error adding limit order TO BOT LIST - clientOid: {limitOrder["clientOid"]}, size:{limitOrder["size"]}, price:{limitOrder["price"]}, orderId: {orderCreationReturn["orderId"]} -', bot)
                            asyncio.sleep(1)

                      else:
                        error = f'Error creating order - {orderCreationReturn["msg"]}'
                        logMessage(LOG_ERROR,error,bot=bot)
                    except Exception as e:
                      error = f'Error creating limit order - maximum: {maximum}, price: {limitOrder["price"]}, message: {str(e)}'
                      logMessage(LOG_ERROR,error,bot=bot)
          else:
            logMessage(LOG_WARN,f'Margin defined for bot not enough to open new orders, available:: {bot.availableMargin}',bot=bot)
        except Exception as e:
          error = f'Error creating order - {str(e)}'
          logMessage(LOG_ERROR,error,bot=bot)

def closePosition(myTrade:MyTradeData,position):
  a=1

def closeBotPosition(myTrade:MyTradeData,position, bot:Bot):
    ret = False
    signal = ( -1 if position['currentQty'] < 0 else 1)
    step = getStepvalue(position['avgEntryPrice'],bot)

    stopOrder =   {
            "clientOid": bot.id+"_"+getUUIDBaseLong()+"_TP",
            "side": "buy" if position['currentQty'] < 0 else "sell",
            "symbol": position['symbol'],
            "type":"limit",
            "size": str(position['currentQty'] * -1) if position['currentQty'] < 0 else str(position['currentQty']),
            "leverage": str(position['realLeverage']),
            "stop": "up" if position['currentQty'] < 0 else "down",
            "price": round(position['avgEntryPrice'] + (step*signal/2), bot.tickerRound),
            "stopPrice": round(position['avgEntryPrice'] + (step*signal/2), bot.tickerRound),
            "stopPriceType": "TP",
            "reduceOnly": True
          }
    try:
      orderCreationReturn = myTrade.createOrder(stopOrder)  
      if not orderCreationReturn['orderId'] is None and orderCreationReturn['orderId'] != '':
        #TODO: Add order to BOT
        ret = True
    except Exception as e:
      logMessage(LOG_ERROR,f'Error closing position {str(e)}',bot=bot)

    return ret

#Ordes may have been missed on a connection error, or system reset
# def deleteWrongOrders( botManager:BotManager, orderList):
#     ordersToDelete = []
#     if len(orderList) > 0:
#       #This is for old orders, and is not ONLINE, has some delay
#       allOrdersHistory = botManager.TM.get_order_list(symbol=botManager.bot.symbol, pageSize=1000, endAt=botManager.bot.dateMiliSeconds)
#       for order in orderList:
#         orderFound = next((x for x in allOrdersHistory['items'] if x['id'] == order['id']), None)
#         if orderFound:
#           ordersToDelete.append(orderFound['id'])
#       deleteOrders(botManager.bot.id,ordersToDelete)
#     return len(ordersToDelete) > 0
#Ordes may have been missed on a connection error, or system reset
def getMissedOrders( botManager:BotManager):
    ordersAdded:List[Order] = []
    lastStartedAt = 0
    if len(botManager.orders) > 0:
      #This is for old orders, and is not ONLINE, has some delay
      allOrdersHistory = botManager.TM.get_order_list(symbol=botManager.bot.symbol, startAt=botManager.status.lastOrderCheck, pageSize=1000)
      currentPage = allOrdersHistory['currentPage']
      totalPage   = allOrdersHistory['totalPage']

      while currentPage < totalPage:
        morePagesOrders = botManager.TM.get_order_list(symbol=botManager.bot.symbol, startAt=botManager.status.lastOrderCheck, pageSize=1000,currentPage=currentPage+1)
        currentPage = morePagesOrders['currentPage']
        totalPage = morePagesOrders['totalPage']
        allOrdersHistory['items'] = allOrdersHistory['items'] + morePagesOrders['items']

      #This is supposed to be online
      allDoneOrders24Hrs = botManager.TM.get_24h_done_order(symbol=botManager.bot.symbol)
      allOrders= allDoneOrders24Hrs
      for historyOrder in allOrdersHistory['items']:
        orderFound = next((x for x in allDoneOrders24Hrs if x['createdAt'] > botManager.status.lastOrderCheck and x['id'] == historyOrder['id']), None)
        if orderFound is None:
          allOrders.append(historyOrder)

      for xOrder in allOrders:        
        if xOrder['clientOid'][:10] == botManager.bot.id : #or xOrder['clientOid'] =="" :#Empty orders is just temporary to add manual orders, REMOVE!
            if not botManager.orderExists(xOrder['id']):
                if xOrder['cancelExist']:
                  status = ORDER_CANCELED
                elif xOrder['size'] == xOrder['filledSize']:
                  status = ORDER_COMPLETED
                elif  xOrder['filledSize'] > 0 :
                  #should never stop here?
                  status = ORDER_PARTIALLY_FILLED
                lastStartedAt = xOrder['createdAt']  if xOrder['createdAt'] > lastStartedAt else lastStartedAt
                x = Order(clientOid=xOrder['clientOid'], orderId=xOrder['id'], status = status , type= "limit" if xOrder['reduceOnly'] else "limit", side=xOrder['side'], reduceOnly=xOrder['reduceOnly'])
                #botManager.orders.append(x)
                ordersAdded.append(x)
    return (ordersAdded,lastStartedAt)
def botChangesDetails(oldBot:Bot,newBot:dict):
  message = ""
  #It can not be simply deactivated! Needs to manage positions
  # if oldBot.active and not newBot["active"]:
  #   message=f"Bot deactivated"
  if not oldBot.active and newBot["active"]:
    message=f"Bot activated"

  ignoreFields  = ['id','active','savePending', 'updateBot','dateMiliSeconds', 'sendToJob']
  onlyReadFields= ['step','stepPercentage','start', 'end', 'date', "leverage","size", "side", 'symbol']

  for field in oldBot.__dict__:
    if field not in ignoreFields:
      if field  in onlyReadFields:
        if newBot[field] != oldBot. __getattribute__(field):
          message= message + f"Field {field} change ignored, field is readOnly\n"
          newBot[field] = oldBot. __getattribute__(field)
      elif newBot[field] != oldBot. __getattribute__(field):
          message= message + f"Field {field} changed from {oldBot. __getattribute__(field)} to { newBot[field] }\n"

  return message
async def main():
  myTrade = MyTradeData(key=API_KEY, secret=API_SECRET, passphrase=passphrase,
                url='https://api-futures.kucoin.com')
  
  #migrateBot(myTrade)
  #copyBotParams(myTrade)
  #copyBotParamsFromOld(myTrade)
  bots  = []
  bots  = getBots(myTrade)
  startTime = current_milli_time()
  accountBalance = 0
  cyclesToCheck = 20
  cycles = 20
  updateAccount = True
  # for bot in bots:
  #   logMessage(LOG_INFO,"Starting bots - Initializing values",bot.symbol)
  #   try: 
  #     logMessage(LOG_INFO,"Starting bots - Finished initializing values",bot.symbol)
  #   except Exception as e:
  #     error = 'Error initializeBotValues::  '+str(e)
  #     logMessage(LOG_ERROR,error)
  for botManager in bots:
      message = f'Updating orders status bot id {botManager.bot.id}, symbol {botManager.bot.symbol}'
      logMessage(LOG_INFO,message, bot=botManager.bot, log_level=LOG_ALWAYS)
      botManager.updateOrdersStatus(resetAllValues=True)
      botManager.updateResults(force=True)
      botManager.checkPendingSaves()
  
  keepRunning = True
  forceResults = False
  while keepRunning:
    if forceResults:
      botManager.updateOrdersStatus(resetAllValues=True)
    #TODO: USE ELAP TIME INSTEAD OF CYCLES
    cycles = cycles + 1
    #Get updated account balance
    try:
      accountBalance = myTrade.getAccountOverView('USDT')
      if updateAccount or cycles > cyclesToCheck:
        message = f' Equity: {round(accountBalance["accountEquity"],2)}\n Unr. PNL: {accountBalance["unrealisedPNL"]}\n Margin Balance: {round(accountBalance["marginBalance"],2)}\n Position Margin: {round(accountBalance["positionMargin"],2)}\n'
        message = message + f' Order Margin: {round(accountBalance["orderMargin"],2)}\n Avl. Balance: {round(accountBalance["availableBalance"],2)}'
        updateAccountStatus(accountBalance)
        logMessage(type=LOG_INFO,message=message, log_level=LOG_ALWAYS)
        cycles = 0
        updateAccount = False
        # for bot in bots:
        #   if cycles >= cyclesToCheck:
        #     cycles = 0
    except Exception as e:
      error = 'Error getting account balance::  '+str(e)
      logMessage(LOG_ERROR,error)
  
    #Check if there are updates in server fot he bots running or for new bots
    try:
        botsToUpdate = getBotsToUpdate()
        for botToUpdate in botsToUpdate:
          if "dateMiliSeconds" not in botToUpdate.keys():
            botToUpdate['dateMiliSeconds']= date_to_milliseconds(botToUpdate["date"][0])
          found = False
          for botManager in bots:      
            if botManager.bot.id == botToUpdate['id']:
                message = botChangesDetails(newBot=botToUpdate,oldBot=botManager.bot)
                botManager.bot = Bot(botToUpdate)
                botManager.bot.sendToJob = False
                botManager.savePending = True
                message = f'Updated bot settings {botManager.bot.symbol}:{botManager.bot.id}\n{message}'
                try:
                  updateBot(botManager.bot)
                  botManager.savePending = False
                  logMessage(LOG_INFO,message,bot=botManager.bot, log_level=LOG_ALWAYS)
                except Exception as e:
                  error = 'Error updating BOT setting on FB::  '+str(e)
                  logMessage(LOG_ERROR,error)
                found = True
                break
          if not found:
            newBot = BotManager(botData=botToUpdate, myTrade=myTrade)
            if newBot.bot.id == '':
                newBot.bot.id = getUUIDBaseLong()
            newBot.status = BotStatus()
            newBot.bot.sendToJob = False
            #This saves new data to BOT, and saves new Grid Items
            try:
              initializeBot(newBot)
              bots.append(newBot)
              message = f'New bot added {botManager.bot.symbol}:{botManager.bot.id}'
              logMessage(LOG_INFO,message,bot=botManager.bot, log_level=LOG_ALWAYS)

            except Exception as e:
              error = 'Error initializing new BOT::  '+str(e)
              logMessage(LOG_ERROR,error)

    except Exception as e:
      error = 'Error getting updated BOTS::  '+str(e)
      logMessage(LOG_ERROR,error)
    #RUN BOTS
    for botManager in bots:     
      if botManager.bot.active:
        try:
          #Get position details to be used on this cylce
          try:
            position = botManager.TM.get_position_details(botManager.bot.symbol)
            #Updates results if there is not position registeres on status
            if position['id'] == '' and botManager.status.currentPositionMargin !=0:
                botManager.updateResults(force=False, positionCalc=position)
                botManager.checkPendingSaves()
          except Exception as e:
            error = 'Error getting position on bot cycle:  '+str(e)
            logMessage(LOG_ERROR,error,bot=botManager.bot)
            position = {}

          #Updates status and send log message if position ROE changes more than 1%
          try: 
            if botManager.status.prevROEPcnt != 0: 
              if abs((position['unrealisedRoePcnt']-botManager.status.prevROEPcnt))*100 > 1:
                # send message if PNL changed more than 1%
                message = f'Position:\n Size:{position["currentQty"]* botManager.bot.tickerMultiplier }\n PNL: {round(position["realisedPnl"]+position["unrealisedPnl"],4) }\nROE: { round(position["unrealisedRoePcnt"]*100,2)}%\nAvg Entry Price: {position["avgEntryPrice"]}'
                message = message + f'\nMarket Price: {position["markPrice"]}'
                botManager.status.prevROEPcnt    = position['unrealisedRoePcnt']
                botManager.status.statusPosition = json.dumps(position)
                botManager.status.totalUpdatePending    = True
                botManager.status.savePending    = True
                logMessage(LOG_INFO,message,bot=botManager.bot)
          except Exception as e:
            error = 'Error checKING ROE STATUS on bot cycle:  '+str(e)
            logMessage(LOG_ERROR,error,bot=botManager.bot)
            position = {}

          botManager.status.prevROEPcnt = position['unrealisedRoePcnt']

          #Gets current price to be used on this cycle
          currPrice = botManager.TM.getMarkPrice(botManager.bot.symbol)['value']
          try:             
            kLines = botManager.TM.getKlines(botManager.bot.symbol,1,startTime)
            length = len(kLines)
            minimum = kLines[length-1][3]
            maximum = kLines[length-1][2]
            startTime = current_milli_time()
          except Exception as e:
            minimum = currPrice #if minimum == 0 else minimum
            maximum = currPrice #if maximum == 0 else maximum

          #Checks if entry price was reached
          if not botManager.bot.entryValueActivated:
            if botManager.bot.side == 'sell':
                if maximum >= botManager.bot.entryValue:
                    botManager.setEntryValueActivated()
            elif botManager.bot.side == 'buy':
                if minimum <= botManager.bot.entryValue:
                    botManager.setEntryValueActivated()

          #TODO: Harcoded para sair se tem menos de 140 USD
          if botManager.bot.entryValueActivated and accountBalance["accountEquity"] < 140 and position["avgEntryPrice"] != 0:
            if closeBotPosition(myTrade, position, botManager.bot):
              keepRunning = False
              logMessage(LOG_INFO,"Closing position and cancelling bot",bot=botManager.bot)
              break
          
          #Only run if entry value was acitvated
          if botManager.bot.entryValueActivated:            
            #check if any missed order
            if (botManager.status.sellSize - botManager.status.buySize + (position["currentQty"]* botManager.bot.tickerMultiplier)) != 0:
                if checkMissedOrders(botManager):
                  botManager.updateOrdersStatus(resetAllValues=True)
                  botManager.updateResults(force=True)
                  botManager.checkPendingSaves()

            #TODO: Checks Position STOP LOSS
            if botManager.bot.positionSLPerc > 0 and position["unrealisedRoePcnt"]<0 and abs(position["unrealisedRoePcnt"]*100) >= botManager.bot.positionSLPerc :
              closePosition(myTrade,position)
            createStopOrders(botManager,botManager.bot,position)
            botManager.updateResults(force=False)

            #Check if there is data to be saved after running CreateStopOrders
            botManager.checkPendingSaves()

            #Release orders margin (above maxGridSteps)
            releaseOrdersMargin(botManager,botManager.bot)
            botManager.updateResults(force=False)

            #If it will update status, ask to update balances also
            if botManager.status.savePending:
              updateAccount = True

            #Check if there is data to be saved after running releaseOrdersMargin
            botManager.checkPendingSaves()
            if position["posInit"] < botManager.bot.maxMargin:
              createLimitOrders(botManager, botManager.bot,accountBalance,startTime, position)
              botManager.updateResults(force=False)
              #Check if there is data to be saved after running createLimitOrders
              botManager.checkPendingSaves()
            else:
              #Protection to only print once on each cycle
              if cycles == 1:
                logMessage(LOG_WARN,f'Position value ({position["posInit"]}) reached maximum margin {botManager.bot.maxMargin} defined',bot=botManager.bot)

            addManualOrdersToBot(botManager, botManager.bot)
            #Check if there is data to be saved after running createLimitOrders
            botManager.checkPendingSaves()

        except Exception as e:
          error = 'Error getting position::  '+str(e)
          logMessage(LOG_ERROR,error,bot=botManager.bot)

    #startTime = current_milli_time()
    await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())