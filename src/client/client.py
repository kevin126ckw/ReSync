#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/09/06 18:35
# @Author  : Kevin Chang
# @File    : client.py
# @Software: PyCharm

from networking import NetworkClient
from src.relib.logger import Logger

logger = Logger(__name__)


class FileClient:
    pass
    
if __name__ == '__main__':

    net = NetworkClient(lambda message: logger.debug(f"收到消息: {message}"))
    # 保持主线程运行
    try:
        net.start_listening()
        net.send_message({"type": "hello", "payload": {"content": "Hello, World!"}})
        # 防止主线程退出
        while True:
            pass
    except KeyboardInterrupt:
        print("Client stopped")