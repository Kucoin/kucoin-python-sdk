import json
import asyncio
import uuid
from kucoin.client import User
from kucoin_futures.client import Trade
from myTradeData import MyTradeData
from secrets_API_KEYS import API_KEY,API_SECRET,TELEGRAM_BOT_KEY,TELEGRAM_CHAT_ID,passphrase
import requests

import time


def sendTelegramMessage(message=''):
    r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=HTML&text={message}")

# client = User(key=API_KEY, secret=API_SECRET, passphrase=passphrase,
#              url='https://openapi-v2.kucoin.com')

#user_page = client.get_sub_user_page()
#print(user_page)

# account_summary_info = client.get_account_summary_info()
# print(account_summary_info)

# stop	String	No	Either down or up. Requires stopPrice and stopPriceType to be defined
# stopPriceType	String	No	Either TP, IP or MP, Need to be defined if stop is specified.
# stopPrice	String	No	Need to be defined if stop is specified.
# trade = Trade(key=API_KEY, secret=API_SECRET, passphrase=passphrase,
#              url='https://api-futures.kucoin.com')

myTrade = MyTradeData(key=API_KEY, secret=API_SECRET, passphrase=passphrase,
              url='https://api-futures.kucoin.com')
#
#fills = myTrade.get_fills_details(symbol='OMNIUSDTM')
#ledger = myTrade.getAccountLedger(symbol='OMNIUSDTM')
bots = []

# bots.append({
#   "symbol" : 'SLERFUSDTM',
#   "start" : 0.37,
#   "step" : 0.003,
#   "end" : 0.445,
#   "entryValue" : 0,
#   "size" : 30,
#   "grids" : 20,
#   "leverage" : "10",
#   "ticker" : 4,
#   "orders": []
# }) (size is in fact size/leverage)
bots.append({
  "symbol" : 'OMNIUSDTM',
  "start" : 22,
  "step" : 0.2,
  "end" : 35,
  "entryValue" : 0,
  "size" : 40,
  "grids" : 80,
  "leverage" : "10",
  "tickerRound" : 4,
  "orders": []
})
botID = "bot_"+str(time.time())
orders = []
for bot in bots:
  start = bot['start']
  step = bot['step']
  end = bot['end']
  start = bot['start']
  symbol = bot['symbol']
  size = bot['size']
  leverage = bot['leverage']
  entryValue = bot['entryValue']
  tickerDef = False
  while not tickerDef:
    try:
      contractInfo = myTrade.getContractDetails(symbol)
      tickerDef = True
    except Exception as e:
        error = 'Error getting ticker::  '+str(e)
        print(error)
        sendTelegramMessage(error)
  tickerDec = contractInfo['tickSize']
  tickerRound =0
  while tickerDec !=1:
    tickerDec = tickerDec * 10
    tickerRound = tickerRound + 1
  bot['tickerRound'] = tickerRound
  for i in range(0,bot['grids']):
    if start+(i*step) <= end:
      bot['orders'].append(  {
        "clientOid":str(uuid.uuid4()),
        "side":"sell",
        "symbol":symbol,
        "type":"limit",
        "remark": botID,
        "price": str(round(start+(i*step),tickerRound)),
        "size": str(size),
        "leverage": leverage,
        "status" : 0,
        "entryValue" : entryValue
      }
  )

# create_market_order(self, symbol, side, clientOid='', **kwargs)
#a= trade.create_market_order(orders[0])

#print(a)
#a= trade.create_market_order(orders[1])
#ordersJson = json.dumps(orders)
prevROEPcnt = 0

orders = bots[0]['orders']
#orders=[]
def current_milli_time():
    return round(time.time() * 1000)

def getTickerDec(symbol):
  tickerDef = False
  while not tickerDef:
    try:
      contractInfo = myTrade.getContractDetails(symbol)
      tickerDef = True
    except Exception as e:
        error = 'Error getting ticker::  '+str(e)
        print(error)
        sendTelegramMessage(error)

  tickerDec = contractInfo['tickSize']
  tickerRound =0
  while tickerDec !=1:
    tickerDec = tickerDec * 10
    tickerRound = tickerRound + 1

  return tickerRound
def changeOrderStatus(orderOid,status):
  for order in orders:
    if order['clientOid'] == orderOid:
      if order['status'] != status:
        order['status'] = status
        break

def cancelOrdersBySide(side, items):
  for order in items:
      if order['side'] == side:
        myTrade.cancelOrderById(order['id'])

def adjustStopOrders():
  global prevROEPcnt
  a= myTrade.get_position_details(symbol)
  b= myTrade.getOpenStopOrderBySymbol(symbol)
  if a['id'] != '':
    if prevROEPcnt != 0: 
      if abs((a['unrealisedRoePcnt']-prevROEPcnt))*100 > 1:
        # send message if PNL changed more than 1%
        message = f'Position symbol [{a["symbol"]}]: size:{a["currentQty"]}, PL: {round(a["realisedPnl"]+a["unrealisedPnl"],4) }, ROE: { round(a["unrealisedRoePcnt"]*100,2)}%'
        print(message)
        sendTelegramMessage(message)
    prevROEPcnt = a['unrealisedRoePcnt']
    if len(b['items']) == 0:
      stopOrder =   {
              "clientOid": "stop"+str(uuid.uuid4()),
              "side": "buy" if a['currentQty'] < 0 else "sell",
              "symbol": a['symbol'],
              "type":"limit",
              "size": str(a['currentQty'] * -1) if a['currentQty'] < 0 else str(a['currentQty']),
              "leverage": str(a['realLeverage']),
              "stop": "down",
              "price": round(a['avgEntryPrice'] - step,tickerRound),
              "stopPrice": round(a['avgEntryPrice'] - step,tickerRound),
              "stopPriceType": "TP",
              "reduceOnly": True
            }
      try:
        c = myTrade.create_bulk_order([stopOrder])  
        message = f'Adjusted TP - size:{stopOrder["size"]} - price:{stopOrder["price"]}'
        print(message)
        sendTelegramMessage(message)
        #TODO: Check if succesfull
      except Exception as e:
        error = 'Error setting TP::  '+str(e)
        print(error)
        sendTelegramMessage(error)

    else:
      for order in b['items']:
        if order['side'] == "buy":
          tickerDec = getTickerDec(order['symbol'])
          if (float(order['stopPrice']) > round(a['avgEntryPrice'],tickerDec) or \
              float(order['stopPrice']) < round(a['avgEntryPrice']-step ,tickerDec) or \
              (order['size']) < ((a['currentQty']) * -1) if a['currentQty'] < 0 else (a['currentQty']) ):
            stopOrder =   {
                    "clientOid":order["clientOid"],
                    "side": order['side'],
                    "symbol": order['symbol'],
                    "type":"limit",
                    "size": str(a['currentQty'] * -1) if a['currentQty'] < 0 else str(a['currentQty']),
                    "leverage": order['leverage'],
                    "stop": "down",
                    "price": round((a['avgEntryPrice'] - step),tickerRound),
                    "stopPrice": round((a['avgEntryPrice'] - step),tickerRound),
                    "stopPriceType": "TP",
                    "reduceOnly": True
                  }
            try:
              cancelOrdersBySide("buy",b['items'])
              c = myTrade.create_bulk_order([stopOrder])
              # Remove STOP prefix for original order
              changeOrderStatus(order["clientOid"][:4],1)
              message = f'Adjusted TP - size:{stopOrder["size"]} - price:{stopOrder["price"]}'
              print(message)
              sendTelegramMessage(message)
              #TODO: Check error return
              #print(c)
              break
            except Exception as e:
              error = 'Error adjusting TP::  '+str(e)
              print(error)
              sendTelegramMessage(error)
  else:
    if prevROEPcnt != 0: 
      message = f'Position symbol [{symbol}] closed, last known ROE: { round(prevROEPcnt*100,2)}%'
      print(message)
      sendTelegramMessage(message)
      prevROEPcnt = 0

async def main():
  startTime = current_milli_time()
  accountBalance = 0
  while True:
    try:
      accountBalance = myTrade.getAccountOverView('USDT')
    except Exception as e:
      error = 'Error getting account balance::  '+str(e)
      print(error)
      sendTelegramMessage(error)
    currPrice = 0
    for order in orders:
      if order['status'] == 2:
        try:
          orderPosition = myTrade.getOrderByOId(order['clientOid'])
          #TODO: Do not add order if there is already a BUY order
          if orderPosition['filledSize'] == float(order['size']):
            stopOrder =   {
                          "clientOid":"stop"+order["clientOid"],
                          "side":"sell" if order['side'] == "buy" else "buy",
                          "symbol": order['symbol'],
                          "type":"limit",
                          "size": order['size'],
                          "leverage": order['leverage'],
                          "stop": "down",
                          "price": str(float(order['price']) - step),
                          "stopPrice": str(float(order['price']) - step),
                          "stopPriceType": "TP",
                          "reduceOnly": True
                        }
            try:
              b = myTrade.create_bulk_order([stopOrder])  
              order['status'] = 1
              message = f'TP created - size:{stopOrder["size"]} - price:{stopOrder["price"]}'
              print(message)
              sendTelegramMessage(message)
              #TODO: Check success response
              #print(b)
            except Exception as e:
              error = 'Error creating TP::  '+str(e)
              print(error)
              sendTelegramMessage(error)
        except Exception as e:
            error = 'Error geting order position::  '+str(e)
            print(error)
            sendTelegramMessage(error)

      if order['status'] == 0:
        try:
          if currPrice ==0:
            currPrice = myTrade.getMarkPrice(order['symbol'])
            try:             
              kLines = myTrade.getKlines(order['symbol'],1,startTime)
              startTime = current_milli_time()
              
              length = len(kLines)
              minimum = kLines[length-1][3]
              maximum = kLines[length-1][2]
            except:
              minimum = currPrice['value']
              maximum = currPrice['value']
          if True: # accountBalance['availableBalance'] > (float(order['price'])/float(order['leverage']) * (float(order['size'])/float(order['leverage'])):
            if order['side'] == 'sell':
              if maximum >= order['entryValue']:
                order['entryValue'] = 0
                # only open up to four grids up
                if float(order['price'])  <  currPrice['value'] + (4.1 * step):
                  if minimum < float(order['price']) - step:
                    b = myTrade.create_bulk_order([order])  
                    if not b[0]['orderId'] is None:
                      order['status'] = 2
                      message = f'Order created - minimum: {minimum}, price: {order["price"]}'
                      print(message)
                      sendTelegramMessage(message)
                      #print(b)
                    else:
                      print(b[0]['msg'])  
            else:
              if minimum <= order['entryValue']:
                order['entryValue'] = 999999
                # only open up to four grids down
                if float(order['price'])  >  currPrice['value'] - (4.1 * step):
                  if maximum > float(order['price']) + step:
                    b = myTrade.create_bulk_order([order])  
                    if not b[0]['orderId'] is None:
                      message = f'Order created - maximum: {maximum}, price: {order["price"]}'
                      print(message)
                      sendTelegramMessage(message)
                      order['status'] = 2
                      #print(b)
                  else:
                    error = f'Error creating order - {b[0]["msg"]}'
                    print(error)
                    sendTelegramMessage(error)
#                    print(b[0]['msg'])
          else:
            print('Balance not enough to open new orders, available:: '+str(accountBalance['availableBalance']))
        except Exception as e:
          error = f'Error creating order - {str(e)}'
          print(error)
          sendTelegramMessage(error)

      if order['status'] == 1:
        try:
          orderPosition = myTrade.getOrderByOId(order['clientOid'])
          if not orderPosition['isActive']:
            print('Order not active, creating again')
            order['status'] = 0
        except:
          print('Order not found')
          order['status'] = 0

      if order['status'] != 0:
        if order['side'] == 'sell':
            # close orders over  four grids up
            if float(order['price'])  >  currPrice['value'] + (5.1 * step):
              orderPosition = myTrade.getOrderByOId(order['clientOid'])
              try:
                myTrade.cancelOrderById(orderPosition['id'])
                order['status'] = 0
                message = f'Canceled over limit order => Order price: {order["price"]}, current price {currPrice["value"]}'
                print(message)
                sendTelegramMessage(message)
              except Exception as e:
                error = 'Error canceling over limit order::  '+str(e)
                print(error)
                sendTelegramMessage(error)
        else:
          if minimum <= order['entryValue']:
            # close orders below four grids down
            if float(order['price'])  <  currPrice['value'] - (5.1 * step):
              orderPosition = myTrade.getOrderByOId(order['clientOid'])
              try:
                myTrade.cancelOrderById(orderPosition['id'])
                order['status'] = 0
                message = f'Canceled below limit order => Order price: {order["price"]}, current price {currPrice["value"]}'
                print(message)
                sendTelegramMessage(message)
              except Exception as e:
                error = 'Error canceling below limit order::  '+str(e)
                print(error)
                sendTelegramMessage(error)


    adjustStopOrders()
    startTime = current_milli_time()
    await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())