#from ast import excepthandler
# from unittest import expectedFailure
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime, timedelta
from binance.helpers import date_to_milliseconds
import os

# //Para instalar o web app
# npm install -g firebase-tools
# firebase login
# firebase init

# firebase deploy

MESSAGE = 1
WARNING = 2
ERROR   = 3
USERID = 'vJUYzOdlXYQiJ1dPiU3byHv5d6I2'
class Firebase:
   def __init__(self):
      # Opening JSON file
      # print(os.getcwd())
      f = open('bot/firebaseConfig.json')
      # returns JSON object as 
      # a dictionary
      firebaseConfig = json.load(f)
      f.close()
      cred = credentials.Certificate("bot/firebaseServiceAccountKucoinBot.json")
      #firebaseConfig = credentials.Certificate("firebaseConfig.json")
      self.app = firebase_admin.initialize_app(cred,options=firebaseConfig['configKucoinBot'])
      self.firestore_db = firestore.client()
      self.logID = ''
      self.lastOrderUpdate = 0
      self.lastTransactionId = {}
      #self.checkLastOrderUpdated()
      

   def update(self,table, record=None, id=None, subrecordCollection=None,subRecord=None,subRecordId=None):
      try:
         if id is None:
            id = str(record['id'])
         if not record is None:
            record['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
         self.logID = id               
         if subRecord is None:
            save = json.dumps(record)
            return self.firestore_db.collection('botrun').document(USERID).collection(table).document(id).set(json.loads(save), merge=True)
         else:
            if subRecordId is None:
               subRecordId = str(subRecord['id'])
            subRecord['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
            save = json.dumps(subRecord)
            return self.firestore_db.collection('botrun').document(USERID).collection(table).document(id).collection(subrecordCollection).document(subRecordId).set(json.loads(save), merge=True)
      except Exception as e:
         print(e)
         return None

   def updateBotOrder(self, botId, orderId, order):
      try:
         record = order.__dict__
         record['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
         save = json.dumps(record)
         return self.firestore_db.collection('botrun').document(USERID).collection('cryptoBot').document(botId).collection('orders').document(orderId).set(json.loads(save), merge=True)
      except Exception as e:
         print(e)
         return None

   def updateBotGrid(self, botId, gridId, grid):
      try:
         record = grid.__dict__
         record['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
         save = json.dumps(record)
         return self.firestore_db.collection('botrun').document(USERID).collection('cryptoBot').document(botId).collection('gridItems').document(gridId).set(json.loads(save), merge=True)
      except Exception as e:
         print(e)
         return None

   def updateBotStatus(self, botId, status):
      try:
         record = status.__dict__
         record['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
         save = json.dumps(record)
         return self.firestore_db.collection('botrun').document(USERID).collection('cryptoBotStatus').document(botId).set(json.loads(save), merge=True)
      except Exception as e:
         print(e)
         return None

   # def updateBotGridItem(self, botID, order = []):
   #    id = order['orderId']
   #    record = order
   #    try:
   #       record['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
   #       save = json.dumps(record)
   #       return self.firestore_db.collection('botrun').document(USERID).collection('bots').document(botID).collection('orders').document(id).set(json.loads(save))
   #    except Exception as e:
   #       print(e)
   #       return None
   # def updateBotFills(self, botId, clientOid, orderId, record):
   #    try:
   #       record['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
   #       save = json.dumps(record)
   #       return self.firestore_db.collection('botrun').document(USERID).collection('bots').document(botId).collection('gridItems').document(clientOid).collection('orders').document(orderId).set(json.loads(save), merge=True)
   #    except Exception as e:
   #       print(e)
   #       return None

   def getRecord(self,table,id):
      snapshots  = self.firestore_db.collection('botrun').document(USERID).collection(table).document(id).get()
      return snapshots.to_dict()

   def list(self,table):
      ret = []
      snapshots = list(self.firestore_db.collection('botrun').document(USERID).collection(table).get())
      if len(snapshots) > 0:
         for item in snapshots:
            ret.append(item.to_dict())
      return ret

   def getActiveBots(self):
      ret = []
      ref = self.firestore_db.collection('botrun').document(USERID).collection("cryptoBot")
      query = ref.where(u'active', u'==', True)
      try:
         bots = query.get()
         if len(bots) > 0:
            for bot in bots:
               ret.append(bot.to_dict())
      except Exception as e:
         ret = []
      return ret
   
   def getBotsToUpdate(self):
      ret = []
      ref = self.firestore_db.collection('botrun').document(USERID).collection("cryptoBot")
      query = ref.where(u'sendToJob', u'==', True)
      try:
         bots = query.get()
         if len(bots) > 0:
            for bot in bots:
               ret.append(bot.to_dict())
      except Exception as e:
         ret = []
      return ret

   def getGridItems(self,botId):
      ret = []
      ref = self.firestore_db.collection('botrun').document(USERID).collection("cryptoBot").document(botId).collection('gridItems')
      try:
         grids = ref.get()
         if len(grids) > 0:
            for grid in grids:
               ret.append(grid.to_dict())
      except Exception as e:
         ret = []
      return ret
   
   def getOrders(self,botId):
      ret = []
      ref = self.firestore_db.collection('botrun').document(USERID).collection("cryptoBot").document(botId).collection('orders')
      try:
         orders = ref.get()
         if len(orders) > 0:
            for order in orders:
               ret.append(order.to_dict())
      except Exception as e:
         ret = []
      return ret

   def getOldBot(self, code=None):
      ret = []
      ref = self.firestore_db.collection('botrun').document(USERID).collection("bots")
      query = ref.where(u'id', u'==', code)
      try:
         bots = query.get()
         if len(bots) > 0:
            for bot in bots:
               ret.append(bot.to_dict())
      except Exception as e:
         ret = []
      return ret

   # def getRecord(self,table):
   #    snapshots = list(self.firestore_db.collection('botrun').document(USERID).collection(table).get())
   #    return snapshots


   def queueOrders(self,orders):
      updated = False
      for order in orders:
         if (order['updateTime'] > self.lastOrderUpdate):
            order['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
            self.update('orders', id=str(order['orderId']),record=order)
            updated = True
      
      if updated:
         self.checkLastOrderUpdated()

   def updateTransactions(self,transactions,symbol):
      for transaction in transactions:
         transaction['__lastUpdate'] = date_to_milliseconds(datetime.utcnow().isoformat())
         self.update('transactions', id=str(transaction['id']),record=transaction)
      
      if len(transactions) > 0:
         self.initTransactions([symbol])


   # def checkLastOrderUpdated(self):
   #    try:
   #       ref = self.firestore_db.collection('botrun').document(USERID).collection("orders")
   #       query = ref.order_by("updateTime", direction=firestore.Query.DESCENDING).limit(1)
   #       lastUpdatedOrder = query.get()
   #       if len(lastUpdatedOrder) > 0:
   #          self.lastOrderUpdate = lastUpdatedOrder[0].to_dict()['updateTime']
   #    except:
   #       self.lastOrderUpdate = 0

   def checkTransaction(self,symbol):
      try:
         ref = self.firestore_db.collection('botrun').document(USERID).collection("transactions")
         query = ref.order_by("id", direction=firestore.Query.DESCENDING).limit(1)
         lastTransaction = query.get()
         if len(lastTransaction) > 0:
            self.lastTransactionId = lastTransaction[0].to_dict()['id']
      except:
         self.lastTransactionId = 0

   def initTransactions(self,symbols):
      for symbol in symbols:
         ref = self.firestore_db.collection('botrun').document(USERID).collection("transactions")
         query = ref.where(u'symbol', u'==', symbol).order_by("id", direction=firestore.Query.DESCENDING).limit(1)
         try:
            lastTransaction = query.get()
            if len(lastTransaction) > 0:
               self.lastTransactionId[symbol] = lastTransaction[0].to_dict()['id']
            else:
               self.lastTransactionId[symbol] = 0
         except Exception as e:
            self.lastTransactionId[symbol] = 0
   def deleteSLENoTrailed(self):
         ref = self.firestore_db.collection('botrun').document(USERID).collection("SLEValuationLog")
         query = ref.where(u'timeToTrail', u'==', False)
         snapshots = query.get()
         delete_batch = self.firestore_db.batch()
         count = 0
         for doc in snapshots:
            delete_batch.delete(doc.reference)
            count += 1
            if count>=300:
               delete_batch.commit()
               delete_batch = self.firestore_db.batch()
               count=0
         delete_batch.commit()

   def deleteOrders(self,orders=[], botId=''):         
      ref = self.firestore_db.collection('botrun').document(USERID).collection('cryptoBot').document(botId).collection('orders')      
      snapshots = ref.get()
      delete_batch = self.firestore_db.batch()
      count = 0
      for oldLog in snapshots:
         delete_batch.delete(oldLog.reference)
         count += 1
         if count>=300:
            delete_batch.commit()
            delete_batch = self.firestore_db.batch()
            count=0
      delete_batch.commit()

   def deleteOldLogs(self,daysBack=2):
      ref = self.firestore_db.collection('botrun').document(USERID).collection("liveBotLog2")
      dateTo = datetime.today() - timedelta(days=daysBack)
      
      query = ref.where(u'date', u'<=', dateTo.isoformat()[0:10])
      snapshots = query.get()
      delete_batch = self.firestore_db.batch()
      count = 0
      for oldLog in snapshots:
         delete_batch.delete(oldLog.reference)
         count += 1
         if count>=300:
            delete_batch.commit()
            delete_batch = self.firestore_db.batch()
            count=0
      delete_batch.commit()

#         oldLog.reference.delete()
      
