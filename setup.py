#!/usr/bin/python
# -*- coding:utf-8 -*-

from setuptools import setup


setup(
    name='kucoin-python',
    version='v1.0.7',
    packages=['kucoin', 'kucoin/base_request', 'kucoin/margin', 'kucoin/market', 'kucoin/trade', 'kucoin/user',
              'kucoin/websocket', 'kucoin/ws_token'],
    license="MIT",
    author='Arthur',
    author_email="arthur.zhang@kucoin.com",
    url='https://github.com/Kucoin/kucoin-python-sdk',
    description="kucoin-api-sdk",
    install_requires=['requests', 'websockets'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
