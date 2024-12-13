from kucoin.asyncio.async_request.async_request import KucoinAsyncRestApi
import warnings


class AsyncLendingData(KucoinAsyncRestApi):

    async def get_currency_information(self, currency):
        """
        Get Currency Information
        see:https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-currency-information
        """
        params = {
            'currency': currency
        }
        return await self._request('GET', '/api/v3/project/list', params=params)

    async def get_interest_rates(self, currency):
        """
        Get Interest Rates
        see https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-interest-rates
        """
        params = {
            'currency': currency
        }
        return await self._request('GET', '/api/v3/project/marketInterestRate', params=params)

    async def subscription(self, currency, interest_rate, size):
        """
        Subscription
        see: https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/subscription
        """
        params = {
            'currency': currency,
            'interestRate': interest_rate,
            'size': size,
        }
        return await self._request('POST', '/api/v3/purchase', params=params)

    async def redemption(self, currency, purchase_order_no, size):
        """
        Redemption
        see: https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/redemption
        """
        params = {
            'currency': currency,
            'purchaseOrderNo': purchase_order_no,
            'size': size,
        }
        return await self._request('POST', '/api/v3/redeem', params=params)

    async def modify_subscription_orders(self, currency, purchase_order_no, interest_rate):
        """
        Modify Subscription Orders
        see: https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/modify-subscription-orders
        """
        params = {
            'currency': currency,
            'purchaseOrderNo': purchase_order_no,
            'interestRate': interest_rate,
        }
        return await self._request('POST', '/api/v3/lend/purchase/update', params=params)

    async def get_redemption_orders(self, currency,status, **kwargs):
        """
        Get Redemption Orders
        see https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-redemption-orders
        """
        params = {
            'currency': currency,
            'status': status
        }
        if kwargs:
            params.update(kwargs)
        return await self._request('GET', '/api/v3/redeem/orders', params=params)

    async def get_subscription_orders(self, currency,status, **kwargs):
        """
        Get Subscription Orders
        see https://www.kucoin.com/docs/rest/margin-trading/lending-market-v3-/get-subscription-orders
        """
        params = {
            'currency': currency,
            'status': status
        }
        if kwargs:
            params.update(kwargs)
        return await self._request('GET', '/api/v3/purchase/orders', params=params)
