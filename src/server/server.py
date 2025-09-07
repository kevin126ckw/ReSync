#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/09/06 18:35
# @Author  : Kevin Chang
# @File    : server.py
# @Software: PyCharm

from networking import NetworkServer
from src.relib.logger import Logger

logger = Logger(__name__)

if __name__ == '__main__':
    try:
        server = NetworkServer(lambda message: logger.debug(message))
        server.start()
    except KeyboardInterrupt:
        print("Server stopped")