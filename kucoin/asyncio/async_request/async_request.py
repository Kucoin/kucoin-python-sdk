#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import aiohttp
import hmac
import hashlib
import base64
import time
from uuid import uuid1
from urllib.parse import urljoin


try:
    import pkg_resources

    version = 'v' + pkg_resources.get_distribution("kucoin-python").version
except (ModuleNotFoundError, pkg_resources.DistributionNotFound):
    version = 'v1.0.0'


class KucoinAsyncRestApi(object):


    def __init__(self, key='', secret='', passphrase='', url='', is_v1api=False):
        """
        https://docs.kucoin.com

        :param key: Api Token Id  (Mandatory)
        :type key: string
        :param secret: Api Secret  (Mandatory)
        :type secret: string
        :param passphrase: Api Passphrase used to create API  (Mandatory)
        :type passphrase: string
        """

        if url:
            self.url = url
        else:
            self.url = 'https://api.kucoin.com'

        self.key = key
        self.secret = secret
        self.passphrase = passphrase
        self.is_v1api = is_v1api

    async def _request(self, method, uri, timeout=5, auth=True, params=None):
        uri_path = uri
        data_json = ''
        if method in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append("{}={}".format(key, params[key]))
                data_json += '&'.join(strl)
                uri += '?' + data_json
                uri_path = uri
        else:
            if params:
                data_json = json.dumps(params)

                uri_path = uri + data_json

        headers = {}
        if auth:
            now_time = int(time.time()) * 1000
            str_to_sign = str(now_time) + method + uri_path
            sign = base64.b64encode(
                hmac.new(self.secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
            if self.is_v1api:
                headers = {
                    "KC-API-SIGN": sign,
                    "KC-API-TIMESTAMP": str(now_time),
                    "KC-API-KEY": self.key,
                    "KC-API-PASSPHRASE": self.passphrase,
                    "Content-Type": "application/json"
                }
            else:
                passphrase = base64.b64encode(
                    hmac.new(self.secret.encode('utf-8'), self.passphrase.encode('utf-8'), hashlib.sha256).digest())
                headers = {
                    "KC-API-SIGN": sign,
                    "KC-API-TIMESTAMP": str(now_time),
                    "KC-API-KEY": self.key,
                    "KC-API-PASSPHRASE": passphrase,
                    "Content-Type": "application/json",
                    "KC-API-KEY-VERSION": "2"
                }
        headers["User-Agent"] = "kucoin-python-sdk/" + version
        url = urljoin(self.url, uri)

        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method,
                    url,
                    headers=headers,
                    data=data_json if method not in ['GET', 'DELETE'] else None,
                    timeout=timeout
            ) as response:
                return await self.check_response_data(response)

    @staticmethod
    async def check_response_data(response):
        if response.status == 200:
            try:
                data = await response.json()
            except ValueError:
                error_text = await response.text()
                raise Exception(f"JSON decoding error: {error_text}")
            else:
                if data and data.get('code'):
                    if data.get('code') == '200000':
                        return data.get('data', data)
                    else:
                        message = data.get('message', response.text())
                        raise Exception(f"API error {data.get('code')}: {message}")
        else:
            error_text = await response.text()
            raise Exception(f"HTTP error {response.status}: {error_text}")

    @property
    def return_unique_id(self):
        return ''.join([each for each in str(uuid1()).split('-')])
