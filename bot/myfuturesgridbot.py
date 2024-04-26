import json
import asyncio
from operator import contains
import uuid
from kucoin.client import User
from kucoin_futures.client import Trade
from myTradeData import MyTradeData
from secrets_API_KEYS import API_KEY,API_SECRET,passphrase
from datetime import datetime

from myfuncs import current_milli_time, logMessage, getUUIDBaseLong,updateBot,updateBotItems,updateBotItemsOrders,getMyBots
from myfuncs import LOG_INFO, LOG_DEBUG, LOG_WARN, LOG_ERROR

from bot2.botClass import Bot
ORDER_TP_CREATED = 2
ORDER_LIMIT_CREATED = 1
ORDER_WAITING = 0



def changegridItemStatus(clientOId,status, bot, msg=''):
  for order in bot["gridItems"]:
    if order['clientOid'] == clientOId:
      if order['status'] != status:
        order['status'] = status
        order['msg'] = msg
        updateBotItems(botId=bot['id'],gridItem={"id":clientOId,"status":status, "msg": msg})
        break
def mergeFills(bot,b):
  for fillItem in b:
    if not fillItem in bot['fills']:
      bot['fills'].append(fillItem)
  return
def updateBotResults(myTrade:MyTradeData,bot, positionCalc=None):
  orders = []
  if not positionCalc is None:
    position = positionCalc
  else:
    try:
      position = myTrade.get_position_details(symbol= bot["symbol"])
    except Exception as e:
      logMessage(LOG_ERROR,f"Error getting position on bot update {str(e)}")

  bot["fees"]=0
  bot["sellOrders"]=0
  bot["buyOrders" ]=0
  bot["sellValue" ]=0
  bot["buyValue"  ]=0
  bot["realizedPNL"]=0
  bot["unRealizedPNL"]=0
  bot["currentPostionMargin"]=0
  bot["availableMargin"] = bot["maxMargin"]
  bot["ordersMargin"] = 0

  for fillItem in bot['fills']:
    if not fillItem['orderId'] in orders:
      orders.append(fillItem['orderId'])
      bot[fillItem["side"]+"Orders"] = bot[fillItem["side"]+"Orders"]+1
    bot[fillItem["side"]+"Value"] = bot[fillItem["side"]+"Value"]+ float(fillItem["value"])
    bot["fees"] = bot["fees"]+float(fillItem["fee"])
  if position["currentCost"] > 0:
    bot["buyValue"] = bot["buyValue"] - position["currentCost"] 
  else:
    bot["sellValue"] = bot["sellValue"] + position["currentCost"] 

  bot["realizedPNL"] = (bot["sellValue"] - bot["buyValue"]) - bot["fees"] 
  bot["unRealizedPNL"]       = position["unrealisedPnl"]
  bot["currentPostionMargin"]= position["currentCost"]
  openOrders = myTrade.get_order_list(status="active",side=bot["side"], symbol=bot["symbol"])
  for item in openOrders['items']:
    bot["ordersMargin"] = bot["ordersMargin"] + (float(item["value"])/float(item["leverage"]))
  bot["ordersMargin"] = round(bot["ordersMargin"],2)
  bot["availableMargin"] = round(bot["availableMargin"] + (bot["realizedPNL"] if bot['addPNLToMarginAvailable'] is not None and bot['addPNLToMarginAvailable'] else 0) - bot["ordersMargin"],2)

  bot["realizedROE"]=((bot["maxMargin"]+bot["realizedPNL"]) / bot["maxMargin"])-1
  bot["totalROE"]= ((bot["maxMargin"]+bot["realizedPNL"]+bot["unRealizedPNL"]) / bot["maxMargin"])-1
  bot["totalPNL"]=bot["unRealizedPNL"]+bot["realizedPNL"]
  
  return
  # "sellOrders":0,
  # "buyOrders" :0,
  # "sellValue" :0,
  # "buyValue"  :0,
  # "realizedPNL":0,
  # "unRealizedPNL":0,
  # "currentPostionMargin":0

def getStepvalue(price, bot):
  if bot['stepPercentage'] != 0:
    step = (price * (bot['stepPercentage']/100)) /float(bot['leverage'])
  else:
    step = bot['step']
  
  return step

def cancelOrder(myTrade:MyTradeData,bot,orderId = '',  clientOId=''):
    hasChanged = False
    try:
      if clientOId !='' and orderId == '':
        orderServer  =myTrade.getOrderByOId(oid=clientOId)
        orderId=orderServer['id'] 
      elif clientOId =='' and orderId != '':
        orderServer  =myTrade.get_order_details(id=orderId)
        clientOId=orderServer['clientOid'] 
      a = myTrade.cancelOrderById(orderId)
      if len(a['cancelledOrderIds']) > 0:
        for order in bot['adjustedOrders']:
          if order['orderId'] == orderId and order['active']:
              order['msg'] = 'canceled'
              order['active'] = False
              updateBotItemsOrders(botId=bot['id'],gridItemId=clientOId,orderId=orderId,record={"msg":"canceled","active":False})
              hasChanged= True
              break
        for item in bot["gridItems"]:
          if item['clientOid'] == clientOId: 
            for order in item["orders"]:
              if order['orderId'] == orderId and order['active']:
                order['msg'] = 'canceled'
                order['active'] = False
                updateBotItemsOrders(botId=bot['id'],gridItemId=clientOId,orderId=orderId,record={"msg":"canceled","active":False})
                hasChanged= True
                break
        if hasChanged:
          updateBotResults(myTrade,bot)
          updateBot(bot)
        return True
      else:
        error = f'Error canceling order id {orderId}, message {a["msg"]}'
        logMessage(LOG_ERROR,error)        
    except Exception as e:
      error = f'Error canceling order id {orderId}, error {str(e)}'
      logMessage(LOG_ERROR,error)
    return False
def cancelOrdersBySide(myTrade:MyTradeData, side, bot, items):
  #tODO: Cancel order in both SubordersList
  for order in items:
      if order['side'] == side:
        cancelOrder(myTrade, bot, order['id'], order['clientOid'])


def adjustStopOrders(myTrade: MyTradeData, bot):
  hasChanged = False
  try:
    a= myTrade.get_position_details(bot['symbol'])
    stopOrders= {"items":[]}
    openStopOrders= {"items":[]}
    # Get Filled stop orders
    try:
      filledStopOrders = myTrade.get_order_list(status="active",side="buy" if a['currentQty'] < 0 else "sell", symbol=bot["symbol"])
      for stopOrderTmp in filledStopOrders["items"]:
        if stopOrderTmp["reduceOnly"]:
          stopOrders["items"].append(stopOrderTmp)
    except Exception as e:
      logMessage(LOG_ERROR,f'Error getting TP Active order list:: {str(e)}')
    # Get OPEN stop orders
    try:
      openStopOrders =  myTrade.getOpenStopOrderBySymbol(bot['symbol'])
    except Exception as e:
      logMessage(LOG_ERROR,f'Error getting TP OPEN order list:: {str(e)}')
    
    stopOrders["items"]= stopOrders["items"] + openStopOrders["items"]
    step = getStepvalue(a['avgEntryPrice'],bot)
    if a['id'] != '':
      if bot['prevROEPcnt'] != 0: 
        if abs((a['unrealisedRoePcnt']-bot['prevROEPcnt']))*100 > 1:
          # send message if PNL changed more than 1%
          message = f'Position:\n Size:{a["currentQty"]}\n PNL: {round(a["realisedPnl"]+a["unrealisedPnl"],4) }\nROE: { round(a["unrealisedRoePcnt"]*100,2)}%\nAvg Entry Price: {a["avgEntryPrice"]}'
          message = message + f'\nMarket Price: {a["markPrice"]}'
          message = message + f'\nAprox. TP price: {a["avgEntryPrice"]-bot["step"]}'
          bot['prevROEPcnt'] = a['unrealisedRoePcnt']
          hasChanged = True
          logMessage(LOG_INFO,message, asset=bot['symbol'])
      bot['prevROEPcnt'] = a['unrealisedRoePcnt']
      if len(stopOrders['items']) == 0:
        stopOrder =   {
                "clientOid": bot['id']+"_"+getUUIDBaseLong()+"_SL",
                "side": "buy" if a['currentQty'] < 0 else "sell",
                "symbol": a['symbol'],
                "type":"limit",
                "size": str(a['currentQty'] * -1) if a['currentQty'] < 0 else str(a['currentQty']),
                "leverage": str(a['realLeverage']),
                "stop": "down" if a['currentQty'] < 0 else "up",
                "price": round(a['avgEntryPrice'] - step, bot['tickerRound']),
                "stopPrice": round(a['avgEntryPrice'] - step, bot['tickerRound']),
                "stopPriceType": "TP",
                "reduceOnly": True,
                "remark": bot['id']
              }
        try:
          b = myTrade.createOrder(stopOrder)  
          if not b['orderId'] is None and b['orderId'] != '':
            hasChanged = True
            orderCreated = { "orderId" :b['orderId'], "type":"TP", "active": True, "msg":"created"}
            bot['adjustedOrders'].append(orderCreated)
            logMessage(LOG_WARN,"Position without TP, added TP Order to Bot control",bot['symbol'])
            #addOrderToFB(bot,stopOrder["clientOid"],orderCreated)
  #         order['status'] = ORDER_TP_CREATED
            message = f'Adjusted TP - size:{stopOrder["size"]} - price:{stopOrder["price"]}'
            logMessage(LOG_INFO,message,bot['symbol'])
          else:
            error = f'Error creating adjusted TP - size:{stopOrder["size"]}, price:{stopOrder["price"]}, message: {b["msg"]}'
            logMessage(LOG_ERROR,error,bot['symbol'])

        except Exception as e:
          error = 'Error setting adjusted TP::  '+str(e)
          logMessage(LOG_ERROR,error,bot['symbol'])

      else:
        for order in stopOrders['items']:
          if order['reduceOnly']:
            price = float(order['stopPrice'] if order['stopPrice'] is not None else order['price'])
            if (price > round(a['avgEntryPrice'],bot['tickerRound']) or \
                price < round(a['avgEntryPrice']-step ,bot['tickerRound']) or \
                (order['size']) < ((a['currentQty']) * -1) if a['currentQty'] < 0 else (a['currentQty']) ):
              stopOrder =   {
                      "clientOid": order["clientOid"],
                      "side": order['side'],
                      "symbol": order['symbol'],
                      "type":"limit",
                      "size": str(a['currentQty'] * -1) if a['currentQty'] < 0 else str(a['currentQty']),
                      "leverage": order['leverage'],
                      "stop": "up" if order['side'] == "buy" else "down",
                      "price": round((a['avgEntryPrice'] - step),bot['tickerRound']),
                      "stopPrice": round((a['avgEntryPrice'] - step),bot['tickerRound']),
                      "stopPriceType": "TP",
                      "reduceOnly": True,
                      "remark": order['remark']
                    }
              try:
                cancelOrdersBySide(myTrade, order['side'],bot, stopOrders['items'])
                hasChanged = True
                b = myTrade.createOrder(stopOrder)
                if not b['orderId'] is None and b['orderId'] != '':
                  orderCreated = { "orderId" :b['orderId'], "type":"TP", "active": True, "msg":"created"}
                  oIdOrig = order["clientOid"][:-3]
                  for orderOnGrid in bot['gridItems']:
                    if orderOnGrid["clientOid"] == oIdOrig:
                      orderOnGrid['orders'].append(orderCreated)
                      updateBotItemsOrders(botId=bot['id'],gridItemId=oIdOrig,orderId=orderCreated['orderId'],record=orderCreated)
                      break
                  #addOrderToFB(bot,stopOrder["clientOid"],orderCreated)
                  changegridItemStatus(clientOId=stopOrder["clientOid"],status=ORDER_LIMIT_CREATED,bot=bot)
                  details = f'Stop Order Price: {price}\nAvg Entry Price:{round(a["avgEntryPrice"],bot["tickerRound"])}\n'
                  details = details + f'Order TP Size:{order["size"]}\nPosition Size {((a["currentQty"]) * -1) if a["currentQty"] < 0 else (a["currentQty"]) }'
                  message = f'Adjusted TP - size:{stopOrder["size"]} - price:{stopOrder["price"]}\n'+details
                  logMessage(LOG_INFO,message,bot['symbol'])
                else:
                  error = f'Error creating adjusted TP - size:{stopOrder["size"]}, price:{stopOrder["price"]}, message: {b["msg"]}'
                  logMessage(LOG_ERROR,error)
              except Exception as e:
                error = 'Error adjusting TP::  '+str(e)
                logMessage(LOG_ERROR,error,bot['symbol'])
    else:
      if bot["prevROEPcnt"] != 0: 
        message = f'Position symbol [{bot["symbol"]}] closed, last known ROE: { round(bot["prevROEPcnt"]*100,2)}%'
        hasChanged = True
        logMessage(LOG_INFO,message,bot['symbol'])
        bot["prevROEPcnt"] = 0
  except Exception as e:
    error = 'Error checking stop orders:  '+str(e)
    logMessage(LOG_ERROR,error,bot['symbol'])
  
  if hasChanged:  
    updateBotResults(myTrade=myTrade,bot=bot,positionCalc=a)
    updateBot(bot)


def getBots(myTrade:MyTradeData):

  bots = getMyBots()
  # for bot in bots:
  #      x = Bot(bot, myTrade)
  #      x.tmpRefactor()
  #      print(str(Bot(bot)))
  #    #bots.append(Bot(bot))

  # a=1
  #bots=[]
  # botID = getUUIDBaseLong()
  # bots.append({
  #    "id" : botID,
  #    "date": datetime.utcnow().isoformat(), 
  #    "symbol" : 'MERLUSDTM',
  #    "addPNLToMarginAvailable":True,
  #    "increaseSizeByROE":True,
  #    "active" : True,
  #    "side": "sell",
  #    "start" : 0.65,
  #    "step" : 0,
  #    "end" : 1.15,
  #    "entryValue" : 0,
  #    "size" : 300,
  #    "grids" : 100,
  #    "leverage" : "10",
  #    "tickerRound" : 6,
  #    "gridItems": [],
  #    "adjustedOrders": [],
  #    "prevROEPcnt":0,
  #    "stepPercentage":8,
  #    "maxGridSteps":4,
  #    "fills":[],
  #    "maxMargin": 100,
  #    "availableMargin": 100,
  #    "orderCount":0,
  #    "fees":0,
  #    "sellOrders":0,
  #    "buyOrders" :0,
  #    "sellValue" :0,
  #    "buyValue"  :0,
  #    "realizedPNL":0,
  #    "unRealizedPNL":0,
  #    "currentPostionMargin":0,
  #    "ordersMargin":0
  #    realizedROE
#    bot["totalROE"]= ((bot["maxMargin"]+bot["realizedPNL"]+bot["unRealizedPNL"]) / bot["maxMargin"])-1
#  bot["totalPNL"]=bot["unRealizedPNL"]+bot["realizedPNL"]

  #  })
  for bot in bots:
    if bot['fills'] is None:
      bot['fills'] = []
    if bot['gridItems'] is None:
      bot['gridItems'] = []
    if bot['adjustedOrders'] is None:
      bot['adjustedOrders'] = []
    bot['stepPercentage'] = 8
    if len(bot['gridItems']) == 0:
      botID = bot['id']
      start = bot['start']
      step  = bot['step']
      end   = bot['end']
      start = bot['start']
      symbol= bot['symbol']
      size  = bot['size']
      leverage  = bot['leverage']
      entryValue= bot['entryValue']
      tickerDef = False
      while not tickerDef:
        try:
          contractInfo = myTrade.getContractDetails(symbol)
          tickerDef    = True
        except Exception as e:
            error = 'Error getting ticker::  '+str(e)
            logMessage(LOG_ERROR,error,asset=bot['symbol'])
      tickerDec = contractInfo['tickSize']
      tickerRound =0
      while tickerDec <1:
        tickerDec   = tickerDec * 10
        tickerRound = tickerRound + 1
      bot['tickerRound'] = tickerRound
      tickerMult = contractInfo['multiplier']
      tickerMultRound =0
      while tickerMult <1:
        tickerMult   = tickerDec * 10
        tickerMultRound = tickerMultRound + 1
      if tickerMultRound > 0:
        tickerMultRound = tickerMultRound - 1
      bot['tickerMultiplierRound'] = tickerMultRound
      price = start
      # add BOT to FB
      updateBot(bot)

      for i in range(0,bot['grids']):
        id = botID + "_"+ getUUIDBaseLong(i)
        step = getStepvalue(price,bot)
        if price <= end:
          gridItem = {
            "clientOid":id,
            "id": id,
            "side":"sell",
            "symbol":symbol,
            "type":"limit",
            "remark": botID,
            "price": str(round(price,tickerRound)),
            "size": str(size),
            "leverage": leverage,
            "status" : ORDER_WAITING,
            "entryValue" : entryValue,
            "step": step,
            "orders":[],
          }
          updateBotItems(bot['id'],gridItem)
          bot['gridItems'].append(gridItem)
        price = price + step
      updateBot(bot)

  return bots
def runBot(myTrade:MyTradeData,bot,accountBalance,startTime):
  currPrice = 0
  hasChanged = False
  for order in bot["gridItems"]:    
    #Create Take Profit order if already created the limit order
    if order['status'] == ORDER_LIMIT_CREATED:
      try:
        orderPosition = myTrade.getOrderByOId(oid=order['clientOid'])
        #Do not add order if it will trigger imediately
        if orderPosition['filledSize'] == float(order['size']):
          if currPrice ==0:
            currPrice = myTrade.getMarkPrice(order['symbol'])['value']
          if (order['side'] == "sell"):
            orderPrice = float(order['price']) - order['step']
            if currPrice < orderPrice:
              orderPrice = 0
          else:
            orderPrice = float(order['price']) + order['step']
            if currPrice > orderPrice:
              orderPrice = 0            
          if orderPrice > 0:
            size =  order['lastOpenSize']
            stopOrder =   {
                          "clientOid":order["clientOid"]+"_SL",
                          "side":"sell" if order['side'] == "buy" else "buy",
                          "symbol": order['symbol'],
                          "type":"limit",
                          "size": size,
                          "leverage": order['leverage'],
                          "stop": "up" if order['side'] == "buy" else "down",
                          "price": str(orderPrice),
                          "stopPrice": str(orderPrice),
                          "stopPriceType": "TP",
                          "reduceOnly": True,
                          "remark": order['remark']
                        }
            try:
              b = myTrade.createOrder(stopOrder)  
              if not b['orderId'] is None and b['orderId'] != '':
                hasChanged = True
                orderCreated = { "orderId" :b['orderId'], "type":"TP", "active": True, "msg":"created"}
                order['orders'].append(orderCreated)
                #oIdOrig = order["clientOid"][:-3]
                changegridItemStatus(clientOId=order['clientOid'],status=ORDER_TP_CREATED, bot=bot)
                updateBotItemsOrders(botId=bot['id'],gridItemId=order["clientOid"],orderId=orderCreated['orderId'],record=orderCreated)
                #addOrderToFB(bot,stopOrder["clientOid"],orderCreated)
                #order['status'] = ORDER_TP_CREATED
                message = f'TP created - size:{stopOrder["size"]} - price:{stopOrder["price"]}'
                logMessage(LOG_INFO,message,asset=bot['symbol'])
            except Exception as e:
              error = 'Error creating TP::  '+str(e)
              logMessage(LOG_ERROR,error,asset=bot['symbol'])
          else:
            message = f'TP price below (or above) individual TP for this order, ignoring TP creation - size:{order["size"]}, current price: {currPrice}'
            logMessage(LOG_INFO,message,asset=bot['symbol'])
          
      except Exception as e:
          error = 'Error getting order position::  '+str(e)
          logMessage(LOG_ERROR,error,asset=bot['symbol'])
    
    #Check if order is still active
    if order['status'] == ORDER_LIMIT_CREATED:
      try:
        orderPosition = myTrade.getOrderByOId(oid=order['clientOid'])
        if not orderPosition['isActive']:
          message = 'Order not active, setting on wait status to be recreated'
          changegridItemStatus(clientOId=order['clientOid'],status=ORDER_WAITING, bot=bot, msg=message)
          logMessage(LOG_INFO,message,asset=bot['symbol'])
      except:
        message = 'Order not found, setting on wait status to be recreated'
        changegridItemStatus(clientOId=order['clientOid'],status=ORDER_WAITING, bot=bot, msg=message)
        logMessage(LOG_INFO,message,asset=bot['symbol'])
        #order['status'] = ORDER_WAITING

    if order['status'] != ORDER_WAITING :
      if order['side'] == 'sell':
          # close orders over  four grids up
          if float(order['price'])  >  currPrice + ((bot['maxGridSteps']+ 1 + 1/10) * order['step']):
            #orderPosition = myTrade.getOrderByOId(order['clientOid'])
            try:
              #myTrade.cancel_order_by_clientOid(order['clientOid'],order['symbol'])
              if cancelOrder(myTrade=myTrade,bot=bot,clientOId=order['clientOid']):
                hasChanged = True
                message = f'Canceled over limit order => Order price: {order["price"]}, current price {currPrice}'
                changegridItemStatus(clientOId=order['clientOid'],status=ORDER_WAITING, bot=bot, msg=message)
                logMessage(LOG_INFO,message,asset=bot['symbol'])
              else:
                message = f'Canceled over limit order failed => Order price: {order["price"]}, current price {currPrice}'
                logMessage(LOG_WARN,message,asset=bot['symbol'])
            except Exception as e:
              error = 'Error canceling over limit order::  '+str(e)
              logMessage(LOG_ERROR,error,asset=bot['symbol'])
      else:
        # close orders below four grids down
        if float(order['price'])  <  currPrice - ((bot['maxGridSteps']+ 1 + 1/10) * order['step']):
          #orderPosition = myTrade.getOrderByOId(order['clientOid'])
          try:
            if cancelOrder(myTrade=myTrade,bot=bot,clientOId=order['clientOid']):
              hasChanged = True
              message = f'Canceled below limit order => Order price: {order["price"]}, current price {currPrice}'
              changegridItemStatus(clientOId=order['clientOid'],status=ORDER_WAITING, bot=bot, msg=message)
              #order['status'] = ORDER_WAITING
              logMessage(LOG_INFO,message,asset=bot['symbol'])
            else:
              message = f'Canceled over limit order failed => Order price: {order["price"]}, current price {currPrice}'
              logMessage(LOG_WARN,message,asset=bot['symbol'])
          except Exception as e:
            error = 'Error canceling below limit order::  '+str(e)
            logMessage(LOG_ERROR,error,asset=bot['symbol'])

    #Create orders
    if order['status'] == ORDER_WAITING:
      try:
        if currPrice ==0:
          currPrice = myTrade.getMarkPrice(order['symbol'])['value']
          try:             
            kLines = myTrade.getKlines(order['symbol'],1,startTime)
            startTime = current_milli_time()
            length = len(kLines)
            minimum = kLines[length-1][3]
            maximum = kLines[length-1][2]
          except:
            minimum = currPrice
            maximum = currPrice
        if True or bot["availableMargin"] > (float(order['price'])/float(order['leverage']))*(float(order['size'])/float(order['leverage'])):
          if order['side'] == 'sell':
            if maximum >= order['entryValue']:
              order['entryValue'] = 0
              # only open up to four grids up
              if float(order['price'])  <  currPrice + ((bot['maxGridSteps']+ 1/10) * order['step']):
                if minimum < float(order['price']) - order['step']:
                  if bot['increaseSizeByROE'] is not None and  bot['increaseSizeByROE'] and bot["realizedROE"] >0 :
                    # Protection against bad calculated ROE
                    if bot["realizedROE"] < 1:
                      if bot["tickerMultiplierRound"] == 0:
                        size = str(int(round(float(order['size']) * (1+bot["realizedROE"]),bot["tickerMultiplierRound"])))
                      else:
                        size =  str(round(float(order['size']) * (1+bot["realizedROE"]),bot["tickerMultiplierRound"]))
                    else:
                      size =  order['size']
                  else:
                    size =  order['size']
                  order['lastOpenSize'] = size
                  limitOrder =   {
                    "clientOid":order["clientOid"],
                    "side": order['side'],
                    "symbol": order['symbol'],
                    "remark": order['remark'],
                    "type":"limit",
                    "size": size,
                    "leverage": order['leverage'],
                    "price": order['price']
                  }
                  try:
                    #b = myTrade.createOrder(limitOrder)  
                    b = myTrade.createOrder(limitOrder)  
                    if not b['orderId'] is None:
                      hasChanged = True
                      #order['status'] = ORDER_LIMIT_CREATED
                      orderCreated = { "orderId" :b['orderId'], "type":"limit", "active": True, "msg":"created"}
                      order['orders'].append(orderCreated)
                      updateBotItemsOrders(botId=bot['id'],gridItemId=order["clientOid"],orderId=orderCreated['orderId'],record=orderCreated)
                      changegridItemStatus(clientOId=order['clientOid'],status=ORDER_LIMIT_CREATED, bot=bot)
                      #addOrderToFB(bot,order["clientOid"],orderCreated)
                      message = f'Order created - minimum: {minimum}, price: {limitOrder["price"]}'
                      logMessage(LOG_INFO,message,asset=bot['symbol'])
                      #print(b)
                    else:
                      if b['code'] == '300018':
                        message = f'Error creating limit order - minimum: {minimum}, price: {limitOrder["price"]}, message: {b["msg"]}\nChanging order status'
                        changegridItemStatus(clientOId=order['clientOid'],status=ORDER_LIMIT_CREATED, bot=bot)
                        logMessage(LOG_WARN,message,asset=bot['symbol'])
                      else:
                        message = f'Error creating limit order - minimum: {minimum}, price: {limitOrder["price"]}, message: {b["msg"]}'
                      logMessage(LOG_ERROR,message,asset=bot['symbol'])
                  except Exception as e:
                    error = f'Error creating limit order - minimum: {minimum}, price: {limitOrder["price"]}, message: {str(e)}'
                    logMessage(LOG_ERROR,error,asset=bot['symbol'])

          else:
            if minimum <= order['entryValue']:
              order['entryValue'] = 999999
              # only open up to four grids down
              if float(order['price'])  >  currPrice - ((bot['maxGridSteps']+ 1/10) *  order['step']):
                if maximum > float(order['price']) +  order['step']:
                  if bot['increaseSizeByROE'] is not None and  bot['increaseSizeByROE'] and bot["realizedROE"] >0 :
                    # Protection against bad calculated ROE
                    if bot["realizedROE"] < 1:
                      if bot["tickerMultiplierRound"] == 0:
                        size = str(int(round(float(order['size']) * (1+bot["realizedROE"]),bot["tickerMultiplierRound"])))
                      else:
                        size =  str(round(float(order['size']) * (1+bot["realizedROE"]),bot["tickerMultiplierRound"]))
                    else:
                      size =  order['size']
                  else:
                    size =  order['size']
                  order['lastOpenSize'] = size
                  limitOrder =   {
                    "clientOid":order["clientOid"],
                    "side": order['side'],
                    "symbol": order['symbol'],
                    "type":"limit",
                    "remark": order['remark'],
                    "size": size,
                    "leverage": order['leverage'],
                    "price": order['price']
                  }               
                  try:   
                    b = myTrade.createOrder(limitOrder)  
                    if not b['orderId'] is None:
                      hasChanged = True
                      orderCreated = { "orderId":b['orderId'], "type":"limit", "active": True, "msg":"created"}
                      order['orders'].append(orderCreated)
                      updateBotItemsOrders(botId=bot['id'],gridItemId=order["clientOid"],orderId=orderCreated['orderId'],record=orderCreated)
                      changegridItemStatus(clientOId=order['clientOid'],status=ORDER_LIMIT_CREATED, bot=bot)
                      #addOrderToFB(bot,order["clientOid"],orderCreated)
                      message = f'Order created - maximum: {maximum}, price: {limitOrder["price"]}'
                      logMessage(LOG_INFO,message,asset=bot['symbol'])
                    else:
                      error = f'Error creating order - {b["msg"]}'
                      logMessage(LOG_ERROR,error)
                  except Exception as e:
                    error = f'Error creating limit order - maximum: {maximum}, price: {limitOrder["price"]}, message: {str(e)}'
                    logMessage(LOG_ERROR,error,asset=bot['symbol'])
        else:
          logMessage(LOG_WARN,f'Margin defined for bot not enough to open new orders, available:: {bot["availableMargin"]}')
      except Exception as e:
        error = f'Error creating order - {str(e)}'
        logMessage(LOG_ERROR,error,asset=bot['symbol'])
  if hasChanged:
    updateBotResults(myTrade=myTrade,bot=bot)
    updateBot(bot)

def initializeBotValues(myTrade:MyTradeData, bot):
  lenFills = len(bot['fills'])
  for order in bot['adjustedOrders']:
      fills = myTrade.get_fills_details(orderId=order['orderId'])
      mergeFills(bot, fills['items'])
  for gridOrders in bot["gridItems"]:
    for order in gridOrders['orders']:
      fills = myTrade.get_fills_details(orderId=order['orderId'])
      mergeFills(bot, fills['items'])
  if lenFills != len(bot['fills']):
    updateBotResults(myTrade=myTrade,bot=bot)
    updateBot(bot)

def checkOrdersStatus(myTrade:MyTradeData, bot):
  hasChanged = False  
  logMessage(LOG_INFO,"Checking orders status",asset=bot['symbol'])
  lenFills = len(bot['fills'])
  for order in bot['adjustedOrders']:
    if order['active']:
        try:
          orderPosition = myTrade.get_order_details(order['orderId'])
          fills = myTrade.get_fills_details(orderId=order['orderId'])
          mergeFills(bot, fills['items'])
          if not orderPosition['isActive']:
            order['active'] = False
            hasChanged = True
            if orderPosition['size'] == orderPosition['filledSize']:
              order['msg']    = 'Updated order status - Filled'
              message = f'Order {order["orderId"]} filled, price:{orderPosition["price"]}, updating bot list'
            elif orderPosition['cancelExist']:
              order['msg']    = 'Updated order status - Canceled'
              if orderPosition['remark'] is None:
                message = f'Order {order["orderId"]} canceled, updating bot list'
              else:
                message = f'Order {order["orderId"]} canceled, updating bot list. Remark {orderPosition["remark"]}'
            else:
              order['msg']    = 'Updated order status - Not active'
              if orderPosition['remark'] is None:
                message = f'Order {order["orderId"]} not active, updating bot list'
              else:
                message = f'Order {order["orderId"]} not active, updating bot list. Remark { orderPosition["remark"]}'          
            logMessage(LOG_INFO,message,asset=bot['symbol'])          
        except Exception as e:
          error = 'Error getting orders status::  '+str(e)
          logMessage(LOG_ERROR,error,asset=bot['symbol'])

          #order['status'] = ORDER_WAITING
  for gridOrders in bot["gridItems"]:
    for order in gridOrders['orders']:
      if order['active']:
        try: 
          orderPosition = myTrade.get_order_details(order['orderId'])
          fills = myTrade.get_fills_details(orderId=order['orderId'])
          mergeFills(bot, fills['items'])
          if not orderPosition['isActive']:
            hasChanged = True
            order['active'] = False
            if orderPosition['size'] == orderPosition['filledSize']:
              order['msg']    = 'Updated order status - Filled'
              message = f'Order {order["orderId"]} filled, price:{orderPosition["price"]}, updating bot list'
            elif orderPosition['cancelExist']:
              order['msg']    = 'Updated order status - Canceled'
              if orderPosition['remark'] is None:
                message = f'Order {order["orderId"]} canceled, updating bot list'
              else:
                message = f'Order {order["orderId"]} canceled, updating bot list. Remark {orderPosition["remark"]}'
            else:
              order['msg']    = 'Updated order status - Not active'
              if orderPosition['remark'] is None:
                message = f'Order {order["orderId"]} not active, updating bot list'
              else:
                message = f'Order {order["orderId"]} not active, updating bot list. Remark { orderPosition["remark"]}'
            updateBotItemsOrders(bot['id'], gridItemId=gridOrders['clientOid'], orderId=order['orderId'], record=order)
            orderPosition = myTrade.getOrderByOId(gridOrders['clientOid'])
            if not orderPosition['isActive']:
              changegridItemStatus(clientOId=gridOrders['clientOid'],status=ORDER_WAITING, bot=bot, msg=message)
            logMessage(LOG_INFO,message,asset=bot['symbol'])
            #order['status'] = ORDER_WAITING
        except Exception as e:
          error = 'Error getting orders status::  '+str(e)
          logMessage(LOG_ERROR,error,asset=bot['symbol'])

  if lenFills != len(bot['fills']):
    hasChanged = True
  if hasChanged:
    updateBotResults(myTrade=myTrade,bot=bot)
    updateBot(bot)

async def main():
  myTrade = MyTradeData(key=API_KEY, secret=API_SECRET, passphrase=passphrase,
                url='https://api-futures.kucoin.com')
  bots  = []
  bots  = getBots(myTrade)
  startTime = current_milli_time()
  accountBalance = 0
  cyclesToCheck = 20
  cycles = 0
  for bot in bots:
    logMessage(LOG_INFO,"Starting bots - Initializing values",bot['symbol'])
    try: 
      #initializeBotValues(myTrade=myTrade, bot=bot)
      logMessage(LOG_INFO,"Starting bots - Finished initializing values",bot['symbol'])
    except Exception as e:
      error = 'Error initializeBotValues::  '+str(e)
      logMessage(LOG_ERROR,error)

  while True:
    cycles = cycles + 1
    try:
      accountBalance = myTrade.getAccountOverView('USDT')
      if cycles >= cyclesToCheck:
        message = f'Equity: {round(accountBalance["accountEquity"],2)}\nUnr. PNL: {accountBalance["unrealisedPNL"]}\nMargin Balance: {round(accountBalance["marginBalance"],2)}\nPosition Margin: {round(accountBalance["positionMargin"],2)}\n'
        message = message + f'Order Margin: {round(accountBalance["orderMargin"],2)}\nAvl. Balance: {round(accountBalance["availableBalance"],2)}'
        logMessage(LOG_INFO,message)
        for bot in bots:
          if cycles >= cyclesToCheck:
            cycles = 0
            checkOrdersStatus(myTrade, bot)
    except Exception as e:
      error = 'Error getting account balance::  '+str(e)
      logMessage(LOG_ERROR,error)
    
    for bot in bots:
      adjustStopOrders(myTrade, bot)
      runBot(myTrade,bot,accountBalance,startTime)

    startTime = current_milli_time()
    await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())