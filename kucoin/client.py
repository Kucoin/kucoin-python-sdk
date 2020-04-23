from kucoin.margin.margin import MarginData
from kucoin.market.market import MarketData
from kucoin.trade.trade import TradeData
from kucoin.user.user import UserData
from kucoin.ws_token.token import GetToken


class User(UserData):
    pass


class Trade(TradeData):
    pass


class Market(MarketData):
    pass


class Margin(MarginData):
    pass


class WsToken(GetToken):
    pass


