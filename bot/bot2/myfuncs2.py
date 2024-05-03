from copy import copy
import string
import time
import requests
import json
from datetime import datetime
from firebaseConn2 import Firebase
from structs import Bot, BotStatus, Order, GridItem

from typing import Optional

import dateparser
import pytz

db:Firebase = Firebase()

from secrets_API_KEYS import TELEGRAM_BOT_KEY,TELEGRAM_CHAT_ID,TELEGRAM_BOT_KEY_WARN,TELEGRAM_CHAT_ID_WARN
LOG_ALWAYS= -10
LOG_INFO = 1
LOG_WARN = 5
LOG_ERROR= 10
LOG_DEBUG= 99

digs = string.digits + string.ascii_letters
seq = 0
baseDate  = datetime.fromisoformat('2024-01-01')

def getRecord(table:string,id:string):
    return db.getRecord(table=table,id=id)

def updateAccountStatus(accountStatus:dict):
    record = accountStatus
    db.update(table='accountStatus', record=record, id='0')
    return

def updateBot(bot:Bot):
    record = copy(bot.__dict__)        
    db.update(table='cryptoBot', record=record, id=bot.id)
    return

def updateBotGrid(botId:string,gridId:string,gridItem:GridItem):
    db.updateBotGrid(botId, gridId, gridItem)
    return

def updateBotStatus(botId:string,status:BotStatus):
    db.updateBotStatus(botId=botId,status=status)
    return

def updateBotOrder(botId:string,orderId:string,record:Order):
    db.updateBotOrder(botId, orderId, record)
    return

def getMyBots():
    return db.getActiveBots()

def getBotsToUpdate():
    return db.getBotsToUpdate()

def getOldBot(code:string):
    return db.getOldBot(code)

def getGridItems(botId):
    return db.getGridItems(botId)

def getOrders(botId):
    return db.getOrders(botId)

def deleteOrders(botId, orders):
    return db.deleteOrders(orders=orders,botId=botId)

def getStatus(botId):
    return db.getRecord(table="cryptoBotStatus",id=botId)

def getLogType(type):
    if type==LOG_INFO:
        return 'INFO'
    elif type==LOG_WARN:
        return 'WARNING'
    elif type==LOG_ERROR:
        return 'ERROR'
    elif type==LOG_DEBUG:
        return 'DEBUG'
    else:
        return ''

def date_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str, settings={'TIMEZONE': "UTC"})
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)

def fblog(text='', type=LOG_INFO, recordType='message', logTable='livebot2', details={}, fromException=False, asset='', botID=""):
    log = {}
    log["botID"]    = botID
    log['date']     = date_to_milliseconds(datetime.utcnow().isoformat())
    log['recordType']  = 'message'
    log['message']  = text
    log['type']     = type
    log['asset']    = asset
    try:
        log['detail']   = json.dumps(details)
    except:
        try:
            log['detail']   = "{msg:"+json.dumps(details.args)+"}"
        except:
            try:
                log['detail']   = json.dumps(details.__dict__)
            except:
                log['detail']   = {}
    try:
        db.update(record=log, table='liveBotLog2' , id=str(log['date']))
    except Exception as e:
        if not fromException:
            if type(e) == 'string':
                fblog(e,fromException=True)
            else:
                try:
                    fblog('Error on log update',details=e,fromException=True, typeCode=LOG_ERROR )
                except:
                    try:
                        fblog(f'Error on log update {e.msg}',fromException=True, typeCode=LOG_ERROR )
                    except:
                        fblog(f'Error on log update',fromException=True, typeCode=LOG_ERROR )

def sendTelegramMessage(message='', TelegramBot = 'WARN'):
    try:
        if TelegramBot=='WARN':
            r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY_WARN}/sendMessage?chat_id={TELEGRAM_CHAT_ID_WARN}&parse_mode=HTML&text={message}")
        # else:
        #     r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=HTML&text={message}")
    except Exception as e:
        print(f'Error sending Telegram::{str(e)}')

def logMessage( type, message, bot:Bot=None, log_level=-1):
    if bot is None:
        if log_level == -1:               
            log_level = LOG_DEBUG
        asset = ""
        id    = ""
    else:
        if log_level == -1:               
            log_level = bot.log_level
        asset = bot.symbol
        id    = bot.id


    if type >= log_level:
        messageLog = f'[{getLogType(type)}][{asset}]\n{message}'
        
        TelegramBot=''
        if type == LOG_ERROR or type == LOG_WARN:
            TelegramBot='WARN'
        
        sendTelegramMessage(messageLog,TelegramBot=TelegramBot)

        if log_level == LOG_DEBUG:
            messageLog  = f'[{getLogType(type)}][{asset}][{datetime.utcnow().isoformat()}]\n{message}'
            print(messageLog)
        try:
            fblog(text=message,logTable='liveBotLog2' ,type=type, asset=asset, botID=id)
        except Exception as e:
            print(f'Erro updating fb {str(e)}')

def current_milli_time():
    return round(time.time() * 1000)

def getUUIDBaseLong(x=None,lengthID=10):
    global seq
    now       = datetime.utcnow()
    if x is None:
        x= ((now - baseDate).days *60*60*24) + round((now-baseDate).seconds)    
    x   =  x+seq
    seq =  seq+1
    return int2base(x=x,lengthID=10)

def int2base(x, base=len(digs)-1, lengthID=10):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[x % base])
        x = x // base

    if sign < 0:
        digits.append('-')

    digits.reverse()
    ret = ''.join(digits)
    
    return ret.zfill(lengthID)
