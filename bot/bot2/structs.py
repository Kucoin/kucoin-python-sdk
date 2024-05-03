from datetime import datetime
LOG_INFO = 0
LOG_WARN = 5
LOG_ERROR= 10
LOG_DEBUG= 99

class Fill:
    def __init__(self, symbol, orderId, tradeId):
        self.symbol = symbol
        self.tradeId= tradeId
        self.orderId= orderId
        self.side   = ""
        self.liquidity= ""
        self.forceTaker= False
        self.price  = 0 #STR
        self.size   = 0
        self.value  = 0 #STR
        self.openFeePay= 0 #STR
        self.closeFeePay= 0 #STR
        self.stop       = ""
        self.feeRate    = 0 #STR
        self.fixFee     = 0 #STR
        self.feeCurrency= ""
        self.tradeTime  = 0
        self.displayType= ""
        self.fee        = 0 #STR
        self.settleCurrency= ""
        self.orderType  = ""
        self.tradeType  = ""
        self.createdAt  = 0
    def fromObject(self,fill):
        self.side   = fill["side"]
        self.liquidity= fill["liquidity"]
        self.forceTaker= fill["forceTaker"]
        self.price  = float(fill["price"])
        self.size   = fill["size"]
        self.value  = float(fill["value"])
        self.openFeePay= float(fill["openFeePay"])
        self.closeFeePay= float(fill["closeFeePay"])
        self.stop       = fill["stop"]
        self.feeRate    = float(fill["feeRate"])
        self.fixFee     = float(fill["fixFee"])
        self.feeCurrency= fill["feeCurrency"]
        self.tradeTime  = fill["tradeTime"]
        self.displayType= fill["displayType"]
        self.fee        = float(fill["fee"])
        self.settleCurrency= fill["settleCurrency"]
        self.orderType  = fill["orderType"]
        self.tradeType  = fill["tradeType"]
        self.createdAt  = fill["createdAt"]

class Order:
    def __init__(self, order:dict={} , orderId="",price:float=0,type="",side="",status=0,msg="", clientOid="",reduceOnly=False, filledSize=0, filledValue=0):
        self.orderId    =   order["orderId"] if "orderId" in order.keys() else orderId 
        self.id         =   self.orderId
        self.side       =   order["side"] if "side" in order.keys() else side
        self.type       =   order["type"] if "type" in order.keys() else type
        self.msg        =   order["msg"] if "msg" in order.keys() else msg
        self.status     =   order["status"] if "status" in order.keys() else status
        self.clientOid  =   order["clientOid"] if "clientOid" in order.keys() else clientOid
        self.reduceOnly =   order["reduceOnly"] if "reduceOnly" in order.keys() else reduceOnly
        self.filledSize =   order["filledSize"] if "filledSize" in order.keys() else filledSize
        self.filledValue=   order["filledValue"] if "filledValue" in order.keys() else filledValue
        self.price      =   order["price"] if "price" in order.keys() else price

class GridItem:
    def __init__(self, gridItem:dict={}, clientOid="", side="",symbol="",type="",price="",size="",status=0,step=0):
     self.clientOid =   gridItem["clientOid"]   if "clientOid" in gridItem.keys() else clientOid 
     self.id        =   self.clientOid
     self.type      =   gridItem["type"]        if "type" in gridItem.keys() else type 
     self.price     =   gridItem["price"]       if "price" in gridItem.keys() else price 
     self.size      =   gridItem["size"]        if "size" in gridItem.keys() else size 
     self.status    =   gridItem["status"]      if "clientOid" in gridItem.keys() else status 
     self.step      =   gridItem["step"]        if "clientOid" in gridItem.keys() else step 
     self.lastOpenSize =  gridItem["lastOpenSize"] if "lastOpenSize" in gridItem.keys() else ""     

class Bot:
    def __init__(self, bot:dict):
        self.id     = bot["id"]
        self.date               = bot["date"]
        self.dateMiliSeconds    = bot["dateMiliSeconds"]
        self.symbol = bot["symbol"]
        self.addPNLToMarginAvailable=bot["addPNLToMarginAvailable"]
        self.increaseSizeByROE=bot["increaseSizeByROE"]
        self.sendToJob = bot["sendToJob"] if "sendToJob" in bot.keys() else False

        #Position Stop Loss percentage will close position, but Bot will continue running
        self.positionSLPerc = bot["positionSLPerc"] if "positionSLPerc" in bot.keys() else 0

        #SL and TP Perc are relative to MaxMargin
        self.botSLPerc      = bot["botSLPerc"]  if "botSLPerc" in bot.keys() else 0
        self.botTPPerc      = bot["botTPPerc"] if "botTPPerc" in bot.keys() else 0
        
        self.log_level      = bot["log_level"] if "log_level" in bot.keys() else LOG_DEBUG
        self.deactivateBotCommand   = bot["deactivateBotCommand"] if "deactivateBotCommand" in bot.keys() else 0

        self.log_level      = bot["log_level"] if "log_level" in bot.keys() else LOG_DEBUG
        self.active = bot["active"]
        self.side   = bot["side"]
        self.start  = bot["start"]
        self.step   = bot["step"]
        self.end    = bot["end"]
        self.size   = bot["size"]
        self.grids  = bot["grids"]
        self.entryValue = bot["entryValue"]
        self.leverage   = bot["leverage"]
        self.tickerRound= bot["tickerRound"]
        self.tickerMultiplierRound = bot["tickerMultiplierRound"] if "tickerMultiplierRound" in bot.keys() else 2
        self.tickerMultiplier = bot["tickerMultiplier"] if "tickerMultiplier" in bot.keys() else 1
        self.maxMargin  = bot["maxMargin"]
        self.maxGridSteps=bot["maxGridSteps"]
        self.stepPercentage = bot["stepPercentage"]
        self.entryValueActivated = True if self.entryValue == 0 else False
        self.savePending = False
        #To send signal to be updated when something is changed in monitor portal
        self.updateBot   = False
class BotStatus:
    def __init__(self, status:dict= {}):
        self.savePending = False
        self.availableMargin=status["availableMargin"] if "availableMargin" in status.keys() else 0
        self.prevROEPcnt= 0
        self.orderCount = status["orderCount"] if "orderCount" in status.keys() else 0
        self.fees       = status["fees"] if "fees" in status.keys() else 0
        self.sellOrders = status["sellOrders"] if "sellOrders" in status.keys() else 0
        self.buyOrders  = status["buyOrders"] if "buyOrders" in status.keys() else 0
        self.sellValue  = status["sellValue"] if "sellValue" in status.keys() else 0
        self.buyValue   = status["buyValue"] if "buyValue" in status.keys() else 0
        self.sellSize   = status["sellSize"] if "sellSize" in status.keys() else 0
        self.buySize    = status["buySize"] if "buySize" in status.keys() else 0
        self.realizedPNL= status["realizedPNL"] if "realizedPNL" in status.keys() else 0
        self.unRealizedPNL=status["unRealizedPNL"] if "unRealizedPNL" in status.keys() else 0
        self.currentPositionMargin= status["currentPositionMargin"] if "currentPositionMargin" in status.keys() else 0
        self.currentPositionTotalCost= status["currentPositionTotalCost"] if "currentPositionTotalCost" in status.keys() else 0
        self.currentPositionMarginCost= status["currentPositionMarginCost"] if "currentPositionMarginCost" in status.keys() else 0
        self.ordersMargin= status["ordersMargin"] if "ordersMargin" in status.keys() else 0
        self.realizedROE = status["realizedROE"] if "realizedROE" in status.keys() else 0
        self.totalROE    = status["totalROE"] if "totalROE" in status.keys() else 0
        self.totalPNL    = status["totalPNL"] if "totalPNL" in status.keys() else 0
        self.statusPosition = ""
        self.totalUpdatePending  = False
        self.sellOrdersDetail = []
        self.buyOrdersDetail = []
        self.lastOrderCheck  = status["lastOrderCheck"] if "lastOrderCheck" in status.keys() else 0
        
class LedgerItem:
    def __init__(self, item:dict):
        self.time       = item["time"] if "time" in item.keys() else 0
        self.type       = item["type"] if "type" in item.keys() else ""
        self.amount     = item["amount"] if "amount" in item.keys() else 0
        self.fee        = item["fee"] if "fee" in item.keys() else 0
        self.accountEquity = item["accountEquity"] if "accountEquity" in item.keys() else 0
        self.remark     = item["remark"] if "remark" in item.keys() else ""
        self.status     = item["status"] if "status" in item.keys() else ""
        self.offset     = item["offset"] if "offset" in item.keys() else 0
        self.currency   = item["currency"] if "currency" in item.keys() else ""