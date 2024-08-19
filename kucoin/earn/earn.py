from kucoin.base_request.base_request import KucoinBaseRestApi
import warnings


class EarnData(KucoinBaseRestApi):

    def subscribe_to_earn_fixed_income_products(self, productId, amount, accountType):
        """
        Subscribe to Earn Fixed Income Products
        see: https://www.kucoin.com/zh-hant/docs/rest/earn/general/subscribe-to-earn-fixed-income-products
        """
        params = {
            'productId': productId,
            'amount': amount,
            'accountType': accountType,
        }
        return self._request('POST', '/api/v1/earn/orders', params=params)

    def redeem_by_earn_holding_id(self, orderId, amount, fromAccountType=None, confirmPunishRedeem=None):
        """
        Redeem by Earn Holding ID
        see: https://www.kucoin.com/zh-hant/docs/rest/earn/general/subscribe-to-earn-fixed-income-products
        """
        params = {
            'orderId': orderId,
            'amount': amount,
        }
        if fromAccountType:
            params['fromAccountType'] = fromAccountType
        if confirmPunishRedeem:
            params['confirmPunishRedeem'] = confirmPunishRedeem

        return self._request('DELETE', '/api/v1/earn/orders', params=params)

    def get_earn_redeem_preview_by_holding_id(self, orderId, fromAccountType=None):
        """
        Get Earn Redeem Preview by Holding ID
        see https://www.kucoin.com/docs/rest/earn/general/get-earn-redeem-preview-by-holding-id
        """
        params = {
            'orderId': orderId,
        }
        if fromAccountType:
            params['fromAccountType'] = fromAccountType
        return self._request('GET', '/api/v1/earn/redeem-preview', params=params)

    def get_earn_savings_products(self, currency=None):
        """
        Get Earn Savings Products
        see https://www.kucoin.com/docs/rest/earn/kucoin-earn/get-earn-savings-products
        """
        params = {
            'currency': currency,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._request('GET', '/api/v1/earn/saving/products', params=params)

    def get_earn_fixed_income_current_holdings(self, currentPage=None, pageSize=None, productId=None, productCategory=None, currency=None):
        """
        Get Earn Fixed Income Current Holdings
        see https://www.kucoin.com/docs/rest/earn/kucoin-earn/get-earn-fixed-income-current-holdings
        """
        params = {
            'currentPage': currentPage,
            'pageSize': pageSize,
            'productId': productId,
            'productCategory': productCategory,
            'currency': currency
        }
        params = {k: v for k, v in params.items() if v is not None}

        return self._request('GET', '/api/v1/earn/hold-assets', params=params)

    def get_earn_limited_time_promotion_products(self, currency=None):
        """
        Get Earn Limited-Time Promotion Products

        see https://www.kucoin.com/docs/rest/earn/kucoin-earn/get-earn-limited-time-promotion-products
        """
        params = {
            'currency': currency
        }
        params = {k: v for k, v in params.items() if v is not None}

        return self._request('GET', '/api/v1/earn/promotion/products', params=params)

    def get_earn_kcs_staking_products(self, currency=None):
        """
        Get Earn KCS Staking Products
        see https://www.kucoin.com/docs/rest/earn/staking/get-earn-kcs-staking-products
        """
        params = {
            'currency': currency
        }
        params = {k: v for k, v in params.items() if v is not None}

        return self._request('GET', '/api/v1/earn/kcs-staking/products', params=params)

    def get_earn_staking_products(self, currency=None):
        """
        Get Earn Staking Products
        see https://www.kucoin.com/docs/rest/earn/staking/get-earn-staking-products
        """
        params = {
            'currency': currency
        }
        params = {k: v for k, v in params.items() if v is not None}

        return self._request('GET', '/api/v1/earn/staking/products', params=params)

    def get_earn_eth_staking_products(self):
        """
        Get Earn ETH Staking Products
        see https://www.kucoin.com/docs/rest/earn/staking/get-earn-eth-staking-products
        """

        return self._request('GET', '/api/v1/earn/eth-staking/products')
