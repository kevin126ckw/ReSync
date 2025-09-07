#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/9/7 09:42
# @Author  : Kevin Chang
# @File    : networking.py
# @Software: PyCharm

import socket
import threading
import json
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


class NetworkServer:
    def __init__(self, handle_message, host='localhost', port=3829):
        self.handle_message = handle_message
        self.host = host
        self.port = port
        self.logger = Logger(__name__)
        self.server_address = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def handle_client(self, client_socket):
        while True:
            try:
                # 接收长度信息
                length_bytes = client_socket.recv(8)
                if not length_bytes:
                    # 客户端断开连接
                    break

                # 统一使用大端序解析长度
                length = int.from_bytes(length_bytes, byteorder='big')
                self.logger.debug(f"准备接收长度为 {length} 的数据")

                # 根据长度接收数据
                data = b''
                while len(data) < length:
                    chunk = client_socket.recv(length - len(data))
                    if not chunk:
                        break
                    data += chunk

                self.logger.debug(f"实际接收到的数据: {data}")
                self.logger.debug(f"接收到的数据长度: {len(data)}")

                # 检查数据是否完整
                if len(data) != length:
                    self.logger.debug(f"警告: 数据不完整，期望长度 {length}，实际长度 {len(data)}")
                    continue

                # 解析JSON消息
                try:
                    message = json.loads(data.decode())
                    self.logger.debug(f"成功解析JSON消息: {message}")
                except json.JSONDecodeError as e:
                    self.logger.debug(f"JSON解析错误: {e}")
                    self.logger.debug(f"解码后的数据: {data.decode()}")
                    continue

            except Exception as e:
                self.logger.error(f"处理客户端消息时发生错误: {e}")
                break

            if 'message' in locals() and message:
                self.handle_message(message)

    def start(self):
        self.socket.listen(5)
        self.logger.info(f'Server listening on {self.host}:{self.port}')
        while True:
            client_socket, client_address = self.socket.accept()
            self.logger.info(f'New connection from {client_address}')
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def send_message(self, message):
        self.socket.sendall(len(message).to_bytes(8, 'big'))
        self.socket.sendall(json.dumps(message).encode())