from kucoin.asyncio.earn.earn import AsyncEarnData
from kucoin.asyncio.lending.lending import AsyncLendingData
from kucoin.asyncio.margin.margin import AsyncMarginData
from kucoin.asyncio.market.market import AsyncMarketData
from kucoin.asyncio.trade.trade import AsyncTradeData
from kucoin.asyncio.user.user import AsyncUserData


class User(AsyncUserData):
    pass


class Trade(AsyncTradeData):
    pass


class Market(AsyncMarketData):
    pass


class Lending(AsyncLendingData):
    pass

class Earn(AsyncEarnData):
    pass


class Margin(AsyncMarginData):
    pass


