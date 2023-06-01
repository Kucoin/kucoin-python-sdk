from kucoin.base_request.base_request import KucoinBaseRestApi


class UserData(KucoinBaseRestApi):

    def get_actual_fee(self, symbols):
        """
        https://docs.kucoin.top/#actual-fee-rate-of-the-trading-pair
        :param symbols: symbols
        :type: str
        :return:
            {
                "code": "200000",
                "data": [
                    {
                        "symbol": "BTC-USDT",
                        "takerFeeRate": "0.001",
                        "makerFeeRate": "0.001"
                    },
                    {
                        "symbol": "KCS-USDT",
                        "takerFeeRate": "0.002",
                        "makerFeeRate": "0.0005"
                    }
                ]
            }
        """
        params = {
            "symbols": symbols
        }
        return self._request('GET', '/api/v1/trade-fees', params=params)

    def get_base_fee(self):
        """
        https://docs.kucoin.top/#basic-user-fee

        :return:
            {
                "code": "200000",
                "data": {
                    "takerFeeRate": "0.001",
                    "makerFeeRate": "0.001"
                }
            }
        """
        return self._request('GET', '/api/v1/base-fee')

    def get_sub_user(self):
        """
        https://docs.kucoin.com/#get-user-info-of-all-sub-accounts

        :return:
            [{
                "userId": "5cbd31ab9c93e9280cd36a0a",  //subUserId
                "subName": "kucoin1",
                "remarks": "kucoin1"
            },
            {
                "userId": "5cbd31b89c93e9280cd36a0d",
                "subName": "kucoin2",
                "remarks": "kucoin2"
            }
            ]
        """
        return self._request('GET', '/api/v1/sub/user')

    def create_account(self, account_type, currency):
        """
        https://docs.kucoin.com/#create-an-account
        :param account_type: Account type (Mandatory)
        :type: str
        :param currency: Currency (Mandatory)
        :type: str
        :return:
        {
            "id": "5bd6e9286d99522a52e458de"  //accountId
        }
        """
        params = {
            'type': account_type,
            'currency': currency
        }
        return self._request('POST', '/api/v1/accounts', params=params)

    def get_account_list(self, currency=None, account_type=None):
        """
        https://docs.kucoin.com/#list-accounts
        :param currency: Currency (Optional)
        :type: str
        :param account_type: Account type (Optional)
        :type: str
        :return:
        [{
            "id": "5bd6e9286d99522a52e458de",  //accountId
            "currency": "BTC",  //Currency
            "type": "main",     //Account type, including main and trade
            "balance": "237582.04299",  //Total assets of a currency
            "available": "237582.032",  //Available assets of a currency
            "holds": "0.01099". //Hold assets of a currency
        },
        {
            "id": "5bd6e9216d99522a52e458d6",
            "currency": "BTC",
            "type": "trade",
            "balance": "1234356",
            "available": "1234356",
            "holds": "0"
        }]
        """
        params = {}
        if currency:
            params['currency'] = currency
        if account_type:
            params['type'] = account_type
        return self._request('GET', '/api/v1/accounts', params=params)

    def get_account(self, accountId):
        """
        https://docs.kucoin.com/#get-an-account
        :param accountId: ID of the account (Mandatory)
        :type: str
        :return:
        {
            "currency": "KCS",  //Currency
            "balance": "1000000060.6299",  //Total assets of a currency
            "available": "1000000060.6299",  //Available assets of a currency
            "holds": "0". //Hold assets of a currency
        }
        """
        return self._request('GET', '/api/v1/accounts/{accountId}'.format(accountId=accountId))

    def get_account_ledger(self, **kwargs):
        """
        https://docs.kucoin.top/#get-account-ledgers
        :param kwargs: [optional] currency, direction, bizType, startAt, endAt, currentPage , pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 10,
            "totalNum": 3,
            "totalPage": 1,
            "items": [
                {
                    "id": "5bc7f080b39c5c03486eef8c",//unique key
                    "currency": "KCS",  //Currency
                    "amount": "0.0998", //Change amount of the funds
                    "fee": "0",  //Deposit or withdrawal fee
                    "balance": "0",  //Total assets of a currency
                    "bizType": "Withdraw",  //business type
                    "direction": "in",     //side, in or out
                    "createdAt": 1540296039000,  //Creation time
                    "context": {          //Business core parameters

                        "orderId": "5bc7f080b39c5c03286eef8a",
                        "txId": "bf848bfb6736780b930e12c68721ea57f8b0484a4af3f30db75c93ecf16905c9"
                    }
                },
                {
                    "id": "5bc7f080b39c5c03486def8c",//unique key
                    "currency": "KCS",
                    "amount": "0.0998",
                    "fee": "0",
                    "balance": "0",
                    "bizType": "Deposit",
                    "direction": "in",
                    "createdAt": 1540296039000,
                    "context": {

                        "orderId": "5bc7f080b39c5c03286eef8a",
                        "txId": "bf848bfb6736780b930e12c68721ea57f8b0484a4af3f30db75c93ecf16905c9"
                    }
                },
                {
                    "id": "5bc7f080b39c5c03486def8a",//unique key
                    "currency": "KCS",
                    "amount": "0.0998",
                    "fee": "0",
                    "balance": "0",
                    "bizType": "trade exchange",
                    "direction": "in",
                    "createdAt": 1540296039000,
                    "context": {

                        "tradeId": "5bc7f080b3949c03286eef8a",
                        "orderId": "5bc7f080b39c5c03286eef8e",
                        "symbol": "BTC-USD"
                    }
                }
            ]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/accounts/ledgers', params=params)

    def get_account_hold(self, accountId, **kwargs):
        """
        https://docs.kucoin.com/#get-holds
        :param accountId: ID of the account. (Mandatory)
        :type: str
        :param kwargs: [optional] currentPage , pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 10,
            "totalNum": 2,
            "totalPage": 1,
            "items": [
                {
                    "currency": "ETH",  //Currency
                    "holdAmount": "5083",  //Hold amount of a currency
                    "bizType": "Withdraw",     //business type
                    "orderId": "5bc7f080b39c5c03286eef8e", // ID of funds freezed order
                    "createdAt": 1545898567000, //Creation time
                    "updatedAt": 1545898567000。//update time
                },
                {
                    "currency": "ETH",
                    "holdAmount": "1452",
                    "bizType": "Withdraw",
                    "orderId": "5bc7f518b39c5c033818d62d",
                    "createdAt": 1545898567000,
                    "updatedAt": 1545898567000
                }
            ]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/accounts/{accountId}/holds'.format(accountId=accountId), params=params)

    def get_sub_account(self, subUserId):
        """
        https://docs.kucoin.com/#get-account-balance-of-a-sub-account
        :param subUserId: the user ID of a sub-account. (Mandatory)
        :type: str
        :return:
        {
            "subUserId": "5caefba7d9575a0688f83c45",
            "subName": "sdfgsdfgsfd",
            "mainAccounts": [{
                "currency": "BTC",
                "balance": "8",
                "available": "8",
            "holds": "0",
            "baseCurrency": "BTC",
            "baseCurrencyPrice": "1",
            "baseAmount": "1.1"
            }],
            "tradeAccounts": [{
                "currency": "BTC",
                "balance": "1000",
                "available": "1000",
            "holds": "0",
            "baseCurrency": "BTC",
            "baseCurrencyPrice": "1",
            "baseAmount": "1.1"

          }],
          "marginAccounts": [{
            "currency": "BTC",
            "balance": "1.1",
            "available": "1.1",
            "holds": "0",
            "baseCurrency": "BTC",
            "baseCurrencyPrice": "1",
            "baseAmount": "1.1"
          }]
        }
        """
        return self._request('GET', '/api/v1/sub-accounts/{subUserId}'.format(subUserId=subUserId))

    def get_sub_accounts(self):
        """
        https://docs.kucoin.com/#get-the-aggregated-balance-of-all-sub-accounts
        :return:
        [
          {
                "subUserId": "5caefba7d9575a0688f83c45",
                "subName": "kucoin1",
                "mainAccounts": [{
                    "currency": "BTC",
                    "balance": "6",
                    "available": "6",
              "holds": "0",
              "baseCurrency": "BTC",
              "baseCurrencyPrice": "1",
              "baseAmount": "1.1"

                }],
                "tradeAccounts": [{
                    "currency": "BTC",
                    "balance": "1000",
                    "available": "1000",
              "holds": "0",
              "baseCurrency": "BTC",
              "baseCurrencyPrice": "1",
              "baseAmount": "1.1"
            }],
            "marginAccounts": [{
                "currency": "BTC",
                "balance": "1.1",
                "available": "1.1",
                "holds": "0",
                "baseCurrency": "BTC",
                "baseCurrencyPrice": "1",
                "baseAmount": "1.1"
            }]
          }
        ]
        """
        return self._request('GET', '/api/v1/sub-accounts')

    def get_transferable(self, currency, account_type, **kwargs):
        """
        https://docs.kucoin.com/#get-the-transferable
        :param currency: currency (Mandatory)
        :type: str
        :param account_type: The account type (Mandatory)
        :type: str
        :return:
         {
            "currency": "KCS",
            "balance": "0",
            "available": "0",
            "holds": "0",
            "transferable": "0"
        }
        """
        params = {
            'currency': currency,
            'type': account_type
        }
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/accounts/transferable', params=params)

    def transfer_master_sub(self, currency, amount, direction, subUserId, clientOid='', accountType=None,
                            subAccountType=None):
        """
        https://docs.kucoin.com/#transfer-between-master-user-and-sub-user
        :param currency: currency (Mandatory)
        :type: str
        :param amount: Transfer amount, the amount is a positive integer multiple of the currency precision. (Mandatory)
        :type: str
        :param direction: OUT — the master user to sub user,IN — the sub user to the master user. (Mandatory)
        :type: str
        :param accountType: The account type of the master user (Optional)
        :type: str
        :param subAccountType: The account type of the sub user (Optional)
        :type: str
        :param subUserId: the user ID of a sub-account. (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :return:
        {
            "orderId": "5cbd870fd9575a18e4438b9a"
        }
        """
        params = {
            'currency': currency,
            'amount': amount,
            'direction': direction,
            'subUserId': subUserId
        }
        if accountType:
            params['accountType'] = accountType
        if subAccountType:
            params['subAccountType'] = subAccountType
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        return self._request('POST', '/api/v2/accounts/sub-transfer', params=params)

    def inner_transfer(self, currency, from_payer, to_payee, amount, clientOid=''):
        """
        https://docs.kucoin.com/#inner-transfer
        :param currency: currency (Mandatory)
        :type: str
        :param from_payer: Account type of payer (Mandatory)
        :type: str
        :param to_payee: Account type of payee (Mandatory)
        :type: str
        :param amount: Transfer amount, the amount is a positive integer multiple of the currency precision. (Mandatory)
        :type: str
        :param clientOid: Unique order id created by users to identify their orders, e.g. UUID. (Mandatory)
        :type: str
        :return:
        {
            "orderId": "5bd6e9286d99522a52e458de"
        }
        """
        params = {
            'currency': currency,
            'from': from_payer,
            'to': to_payee,
            'amount': amount
        }
        if not clientOid:
            clientOid = self.return_unique_id
        params['clientOid'] = clientOid
        return self._request('POST', '/api/v2/accounts/inner-transfer', params=params)

    def create_deposit_address(self, currency, chain=None):
        """
        https://docs.kucoin.com/#create-deposit-address
        :param currency: currency (Mandatory)
        :type: str
        :param chain: The chain name of currency, e.g. The available value for USDT are OMNI, ERC20, TRC20,default is
        OMNI. This only apply for multi-chain currency, and there is no need for single chain currency. (Optional)
        :type: str
        :return:
        {
            "address": "0x78d3ad1c0aa1bf068e19c94a2d7b16c9c0fcd8b1",
            "memo": "5c247c8a03aa677cea2a251d",   //tag
            "chain": "OMNI"
        }
        """
        params = {
            'currency': currency
        }
        if chain:
            params['chain'] = chain
        return self._request('POST', '/api/v1/deposit-addresses', params=params)

    def get_deposit_addressv2(self, currency, chain=None):
        """
        https://docs.kucoin.com/#get-deposit-addresses-v2
        :param currency: currency (Mandatory)
        :type: str
        :param chain: The chain name of currency, e.g. The available value for USDT are OMNI, ERC20, TRC20,default is
        OMNI. This only apply for multi-chain currency, and there is no need for single chain currency. (Optional)
        :type: str
        :return:
        [{
            "address": "0x78d3ad1c0aa1bf068e19c94a2d7b16c9c0fcd8b1",
            "memo": "5c247c8a03aa677cea2a251d",        //tag
            "chain": "OMNI",
            "contractAddress": ""
        }]
        """
        params = {
            'currency': currency
        }
        if chain:
            params['chain'] = chain
        return self._request('GET', '/api/v2/deposit-addresses', params=params)

    def get_deposit_address(self, currency, chain=None):
        """
        https://docs.kucoin.com/#get-deposit-address
        :param currency: currency (Mandatory)
        :type: str
        :param chain: The chain name of currency, e.g. The available value for USDT are OMNI, ERC20, TRC20,default is
        OMNI. This only apply for multi-chain currency, and there is no need for single chain currency. (Optional)
        :type: str
        :return:
        {
            "address": "0x78d3ad1c0aa1bf068e19c94a2d7b16c9c0fcd8b1",
            "memo": "5c247c8a03aa677cea2a251d",        //tag
            "chain": "OMNI"
        }
        """
        params = {
            'currency': currency
        }
        if chain:
            params['chain'] = chain
        return self._request('GET', '/api/v1/deposit-addresses', params=params)

    def get_deposit_list(self, **kwargs):
        """
        https://docs.kucoin.com/#get-deposit-list
        :param kwargs: [optional] currency, startAt, endAt, status, currentPage, pageSize
        :return:
        {
          "currentPage": 1,
          "pageSize": 5,
          "totalNum": 2,
          "totalPage": 1,
            "items": [{
                "address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
                "memo": "5c247c8a03aa677cea2a251d",
                "amount": 1,
                "fee": 0.0001,
                "currency": "KCS",
                "isInner": false,
                "walletTxId": "5bbb57386d99522d9f954c5a@test004",
                "status": "SUCCESS",
                "remark": "test",
                "createdAt": 1544178843000,
                "updatedAt": 1544178891000
            }, {
                "address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
                "memo": "5c247c8a03aa677cea2a251d",
                "amount": 1,
                "fee": 0.0001,
                "currency": "KCS",
                "isInner": false,
                "walletTxId": "5bbb57386d99522d9f954c5a@test003",
                "status": "SUCCESS",
                "remark": "test",
                "createdAt": 1544177654000,
                "updatedAt": 1544178733000
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/deposits', params=params)

    def get_deposit_list_v1(self, **kwargs):
        """
        https://docs.kucoin.com/#get-v1-historical-deposits-list
        :param kwargs: [optional] currency, startAt, endAt, status, currentPage, pageSize
        :return:
        {
          "currentPage": 1,
          "pageSize": 5,
          "totalNum": 2,
          "totalPage": 1,
            "items": [{
                "address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
                "memo": "5c247c8a03aa677cea2a251d",
                "amount": 1,
                "fee": 0.0001,
                "currency": "KCS",
                "isInner": false,
                "walletTxId": "5bbb57386d99522d9f954c5a@test004",
                "status": "SUCCESS",
                "remark": "test",
                "createdAt": 1544178843000,
                "updatedAt": 1544178891000
            }, {
                "address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
                "memo": "5c247c8a03aa677cea2a251d",
                "amount": 1,
                "fee": 0.0001,
                "currency": "KCS",
                "isInner": false,
                "walletTxId": "5bbb57386d99522d9f954c5a@test003",
                "status": "SUCCESS",
                "remark": "test",
                "createdAt": 1544177654000,
                "updatedAt": 1544178733000
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/hist-deposits', params=params)

    def get_withdrawal_list(self, **kwargs):
        """
        https://docs.kucoin.com/#get-withdrawals-list
        :param kwargs: [optional] currency, status, startAt, endAt, currentPage , pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 10,
            "totalNum": 1,
            "totalPage": 1,
            "items": [{
                "id": "5c2dc64e03aa675aa263f1ac",
                "address": "0x5bedb060b8eb8d823e2414d82acce78d38be7fe9",
                "memo": "",
                "currency": "ETH",
                "amount": 1.0000000,
                "fee": 0.0100000,
                "walletTxId": "3e2414d82acce78d38be7fe9",
                "isInner": false,
                "status": "FAILURE",
                "remark": "test",
                "createdAt": 1546503758000,
                "updatedAt": 1546504603000
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/withdrawals', params=params)

    def get_hist_withdrawal_list(self, **kwargs):
        """
        https://docs.kucoin.com/#get-v1-historical-withdrawals-list
        :param kwargs: [optional] currency, status, startAt, endAt, currentPage , pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 1,
            "totalNum": 2,
            "totalPage": 2,
            "items": [{
                "currency": "BTC",
                "createAt": 1526723468,
                "amount": "0.534",
                "address": "33xW37ZSW4tQvg443Pc7NLCAs167Yc2XUV",
                "walletTxId": "aeacea864c020acf58e51606169240e96774838dcd4f7ce48acf38e3651323f4",
                "isInner": false,
                "status": "SUCCESS"
            }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/hist-withdrawals', params=params)

    def get_withdrawal_quota(self, currency, chain=None):
        """
        https://docs.kucoin.com/#get-withdrawal-quotas
        :param currency:  currency (Mandatory)
        :type: str
        :param chain: The chain name of currency, e.g. The available value for USDT are OMNI, ERC20, TRC20, default is
        OMNI. This only apply for multi-chain currency, and there is no need for single chain currency. (Optional)
        :type: str
        :return:
        {
            "currency": "KCS",
            "limitBTCAmount": "2.0",
            "usedBTCAmount": "0",
            "limitAmount": "75.67567568",
            "remainAmount": "75.67567568",
            "availableAmount": "9697.41991348",
            "withdrawMinFee": "0.93000000",
            "innerWithdrawMinFee": "0.00000000",
            "withdrawMinSize": "1.4",
            "isWithdrawEnabled": true,
            "precision": 8,   //withdrawal precision
            "chain": "OMNI"
        }
        """
        params = {
            'currency': currency
        }
        if chain:
            params['chain'] = chain
        return self._request('GET', '/api/v1/withdrawals/quotas', params=params)

    def apply_withdrawal(self, currency, address, amount, **kwargs):
        """
        https://docs.kucoin.com/#apply-withdraw-2
        :param currency: Currency. (Mandatory)
        :type: str
        :param address: Withdrawal address (Mandatory)
        :type: str
        :param amount: Withdrawal amount, a positive number which is a multiple of the amount precision
            (fees excluded) (Mandatory)
        :type: float
        :param kwargs:  [Optional]  memo, isInner, remark, chain
        :return:
         {
           "withdrawalId": "5bffb63303aa675e8bbe18f9"
         }
        """
        params = {
            'currency': currency,
            'address': address,
            'amount': amount
        }
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/withdrawals', params=params)

    def cancel_withdrawal(self, withdrawalId):
        """
        https://docs.kucoin.com/#cancel-withdrawal
        :param withdrawalId: Path parameter, a unique ID for a withdrawal order  (Mandatory)
        :type: str
        :return:
        """
        return self._request('DELETE', '/api/v1/withdrawals/{withdrawalId}'.format(withdrawalId=withdrawalId))

    def get_sub_user_page(self, **kwargs):
        """
        https://docs.kucoin.com/#get-paginated-list-of-sub-accounts
        :param kwargs: [optional] currentPage , pageSize
        :return:
        {
            "currentPage":1,
            "pageSize":100,
            "totalNum":1,
            "totalPage":1,
            "items":[
                {
                    "userId":"635002438793b80001dcc8b3",
                    "uid":62356,
                    "subName":"margin01",
                    "status":2,
                    "type":4,
                    "access":"Margin",
                    "createdAt":1666187844000,
                    "remarks":null
                }
            ]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v2/sub/user', params=params)

    def get_account_summary_info(self):
        """
        https://docs.kucoin.com/#get-account-summary-info-v2
        :return:
        {
            "level" : 0,
            "subQuantity" : 5,
            "maxDefaultSubQuantity" : 5,
            "maxSubQuantity" : 5,

            "spotSubQuantity" : 5,
            "marginSubQuantity" : 5,
            "futuresSubQuantity" : 5,

            "maxSpotSubQuantity" : 0,
            "maxMarginSubQuantity" : 0,
            "maxFuturesSubQuantity" : 0
        }
        """
        return self._request('GET', '/api/v2/user-info')

    def create_sub_account(self, password, sub_name, access, **kwargs):
        """
        https://docs.kucoin.com/#create-sub-account-v2
        :param password: Password(7-24 characters, must contain letters and numbers, cannot only contain numbers or include special characters)
        :type: str
        :param sub_name: Sub-account name(must contain 7-32 characters, at least one number and one letter. Cannot contain any spaces.)
        :type: str
        :param access: Permission (types include Spot, Futures, Margin permissions, which can be used alone or in combination).
        :type: str
        :param kwargs:  [Optional]  remarks
        :return:
         {
            "uid": 9969082973,
            "subName": "AAAAAAAAAA0007",
            "remarks": "remark",
            "access": "Spot"
         }
        """
        params = {
            'password': password,
            'subName': sub_name,
            'access': access
        }
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v2/sub/user/created', params=params)

    def get_sub_account_api_list(self, sub_name, **kwargs):
        """
        https://docs.kucoin.com/#get-sub-account-spot-api-list
        :param sub_name: Sub-account name.
        :type: str
        :param kwargs: [optional] apiKey
        :return:
        {
            "subName": "AAAAAAAAAAAAA0022",
            "remark": "hytest01-01",
            "apiKey": "63032453e75087000182982b",
            "permission": "General",
            "ipWhitelist": "",
            "createdAt": 1661150291000
        }
        """
        params = {
            'subName': sub_name
        }
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/sub/api-key', params=params)

    def create_apis_for_sub_account(self, sub_name, passphrase, remark, **kwargs):
        """
        https://docs.kucoin.com/#create-spot-apis-for-sub-account
        :param sub_name: Sub-account name(must contain 7-32 characters, at least one number and one letter. Cannot contain any spaces.)
        :type: str
        :param passphrase: Password(Must contain 7-32 characters. Cannot contain any spaces.)
        :type: str
        :param remark: Remarks(1~24 characters)
        :type: str
        :param kwargs:  [Optional]  permission, ipWhitelist, expire
        :return:
         {
            "subName": "AAAAAAAAAA0007",
            "remark": "remark",
            "apiKey": "630325e0e750870001829864",
            "apiSecret": "110f31fc-61c5-4baf-a29f-3f19a62bbf5d",
            "passphrase": "passphrase",
            "permission": "General",
            "ipWhitelist": "",
            "createdAt": 1661150688000
         }
        """
        params = {
            'subName': sub_name,
            'passphrase': passphrase,
            'remark': remark
        }
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/sub/api-key', params=params)

    def modify_sub_account_apis(self, sub_name, api_key, passphrase, **kwargs):
        """
        https://docs.kucoin.com/#modify-sub-account-spot-apis
        :param sub_name: Sub-account name
        :type: str
        :param passphrase: Password of API key
        :type: str
        :param api_key: API-Key(Sub-account APIKey)
        :type: str
        :param kwargs:  [Optional]  permission, ipWhitelist, expire
        :return:
         {
            "subName": "AAAAAAAAAA0007",
            "apiKey": "630329b4e7508700018298c5",
            "permission": "General",
            "ipWhitelist": "127.0.0.1",
         }
        """
        params = {
            'subName': sub_name,
            'passphrase': passphrase,
            'apiKey': api_key
        }
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/sub/api-key/update', params=params)

    def delete_sub_account_apis(self, sub_name, api_key, passphrase):
        """
        https://docs.kucoin.com/#delete-sub-account-spot-apis
        :param sub_name: Sub-account name(The sub-account name corresponding to the API key)
        :type: str
        :param passphrase: Password(Password of the API key)
        :type: str
        :param api_key: API-Key(API key to be deleted)
        :type: str
        :return:
         {
           "subName": "AAAAAAAAAA0007",
           "apiKey": "630325e0e750870001829864"
         }
        """
        params = {
            'subName': sub_name,
            'passphrase': passphrase,
            'apiKey': api_key
        }

        return self._request('DELETE', '/api/v1/sub/api-key', params=params)

    def get_sub_account_page_info(self, **kwargs):
        """
        https://docs.kucoin.com/#get-paginated-sub-account-information
        :param kwargs: [optional] currentPage , pageSize
        :return:
        {
            "currentPage": 1,
            "pageSize": 10,
            "totalNum": 14,
            "totalPage": 2,
            "items": [
                {
                    "subUserId": "635002438793b80001dcc8b3",
                    "subName": "margin03",
                    "mainAccounts": [
                        {
                            "currency": "00",
                            "balance": "0",
                            "available": "0",
                            "holds": "0",
                            "baseCurrency": "BTC",
                            "baseCurrencyPrice": "125.63",
                            "baseAmount": "0"
                        }
                    ]
                }
            ]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v2/sub-accounts', params=params)

    def get_hf_account_ledgers(self, **kwargs):
        """
        https://docs.kucoin.com/spot-hf/#account-ledger-in-high-frequency-trading-accounts
        :param kwargs: [optional] currency, direction, bizType, lastId, limit, startAt, endAt
        :return:
        [
            {
                "id": "42852417537",
                "currency": "CSP",
                "amount": "1.00000000",
                "fee": "0.00000000",
                "balance": "99999986.99999999",
                "accountType": "TRADE_HF",
                "bizType": "TRADE_EXCHANGE",
                "direction": "in",
                "createdAt": "1661347205743",
                "context": "{'symbol':'CSP-USDT','orderId':'6306257dd9180300014c8d47','tradeId':'609522034689'}"
            },
            {
                "id": "42852401152",
                "currency": "CSP",
                "amount": "1.00000000",
                "fee": "0.00000000",
                "balance": "99999985.99999999",
                "accountType": "TRADE_HF",
                "bizType": "TRADE_EXCHANGE",
                "direction": "out",
                "createdAt": "1661347205743",
                "context": "{'symbol':'CSP-USDT','orderId':'63062585d9180300014c8d50','tradeId':'609522034689'}"
            }
        ]
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/hf/accounts/ledgers', params=params)

    def transfer_to_hf_account(self, client_oid, currency, from_payer, amount):
        """
        transfer to the high-frequency account,return high-frequency account info.
        :param client_oid: Client Order Id，a unique identifier created by the user, using UUID is recommended
        :type: str
        :param currency: currency
        :type: str
        :param from_payer: Payment account type: main(main account), trade(trading account), trade_hf(high-frequency trading account)
        :type: str
        :param amount: Transfer amount, the precision is the precision of the currency multiplied by a positive integer
        :type: float
        :return:
        [
            {
                "balance": "3027.25165335",
                "available": "3027.25165335",
                "holds": "0",
                "currency": "USDT",
                "id": "2560047104",
                "type": "trade_hf"
            }
        ]
        """
        params1 = {
            'clientOid': client_oid,
            'currency': currency,
            'from': from_payer,
            'amount': amount,
            'to': 'trade_hf'
        }
        self._request('POST', '/api/v2/accounts/inner-transfer', params=params1)
        params2 = {
            'currency': currency,
            'type': 'trade_hf'
        }
        return self._request('GET', '/api/v1/accounts', params=params2)
