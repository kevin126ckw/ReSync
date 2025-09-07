#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/9/6 21:17
# @Author  : Kevin Chang
# @File    : logger.py
# @Software: PyCharm
import logging


class Logger:
    def __init__(self,name):
        self.logger = logging.getLogger(name)
        logging.basicConfig(level=logging.DEBUG,
                              format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)