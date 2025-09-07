#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 09:41
# @Author  : Kevin Chang
# @File    : networking.py
# @Software: PyCharm

import json
import socket
import threading
from src.relib.logger import Logger

"""
通信协议：
一个完整的数据包在发送时应分为两部分
包体长度（8字节）|包体
而包体则为JSON格式数据，应分为type和payload个字段
type为字符串，而payload为真正的请求负荷
格式：
{"type":"hello","payload":{"content":"Hello, World!"}}
"""


class NetworkClient:
    def __init__(self, handle_message, host='localhost', port=3829):
        self.listen_thread = threading.Thread(target=self._listen_for_messages)
        self.host = host
        self.port = port
        self.logger = Logger(__name__)
        self.handle_message = handle_message
        self.server_address = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect(self.server_address)

    def send_message(self, message):
        # 确保消息是字符串并编码为字节
        if isinstance(message, dict):
            message_str = json.dumps(message)
        else:
            message_str = str(message)

        message_bytes = message_str.encode('utf-8')
        self.logger.debug(f"发送消息: {message}")
        self.logger.debug(f"消息长度: {len(message_bytes)}")

        self.socket.sendall(len(message_bytes).to_bytes(8, 'big'))
        self.socket.sendall(message_bytes)

    def _listen_for_messages(self):
        # 在单独的线程中监听消息
        while True:
            try:
                # 接收长度信息
                length_bytes = self.socket.recv(8)
                if not length_bytes:
                    self.logger.warning("服务器断开连接")
                    break

                # 统一使用大端序解析长度
                length = int.from_bytes(length_bytes, byteorder='big')
                self.logger.debug(f"准备接收长度为 {length} 的数据")

                # 根据长度接收数据
                data = b''
                while len(data) < length:
                    chunk = self.socket.recv(length - len(data))
                    if not chunk:
                        break
                    data += chunk

                self.logger.debug(f"实际接收到的数据: {data}")
                self.logger.debug(f"接收到的数据长度: {len(data)}")

                # 检查数据是否完整
                if len(data) != length:
                    self.logger.warning(f"警告: 数据不完整，期望长度 {length}，实际长度 {len(data)}")
                    continue

                # 解析JSON消息
                try:
                    message = json.loads(data.decode())
                    self.logger.debug(f"成功解析JSON消息: {message}")
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON解析错误: {e}")
                    self.logger.debug(f"原始数据: {data}")
                    self.logger.debug(f"解码后的数据: {data.decode()}")
                    continue

                if 'message' in locals() and message:
                    self.handle_message(message)
            except Exception as e:
                self.logger.error(f"接收消息时发生错误: {e}")
                break

    def start_listening(self):
        self.listen_thread.daemon = True
        self.listen_thread.start()