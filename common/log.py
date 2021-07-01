#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
import os
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

"""
自定义日志模块，按照日期切分

注意：！！下面已经有实例化对象，在其他地方使用时，只要import logger就行了！！
"""


class GetLogger(object):
    """
    自定义logging，方便使用
    """

    def __init__(self, logs_dir=None, logs_level=logging.INFO):
        self.logs_dir = logs_dir  # 日志路径
        self.now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        self.logs_level = logs_level  # 日志级别
        # 日志的输出格式
        self.log_formatter = logging.Formatter(
            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        if logs_dir is None:
            sep = os.sep  # 自动匹配win,mac,linux 下的路径分隔符
            self.logs_dir = os.path.abspath(os.path.join(__file__, f"..{sep}..{sep}logs"))  # 设置日志保存路径

        # 如果logs文件夹不存在，则创建
        if os.path.exists(self.logs_dir) is False:
            os.makedirs(self.logs_dir)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        # 实例化root日志对象
        log_logger = logging.getLogger('root')
        # 设置日志的输出级别
        log_logger.setLevel(self.logs_level)

        # 创建一个handler，用于输出到cmd窗口控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # 设置日志级别
        console_handler.setFormatter(self.log_formatter)  # 设置日志格式
        log_logger.addHandler(console_handler)

        # 建立一个循环文件handler来把日志记录在文件里
        file_handler_info = TimedRotatingFileHandler(
            filename=self.logs_dir + os.sep + 'Info-{}.log'.format(self.now_time),  # 定义日志的存储
            when='MIDNIGHT',
            backupCount=1,  # 最多存放日志的数量
            encoding="UTF-8",  # 使用UTF - 8的编码来写日志
        )
        file_handler_info.setLevel(logging.DEBUG)  # 设置日志级别
        file_handler_info.setFormatter(self.log_formatter)  # 设置日志格式
        log_logger.addHandler(file_handler_info)
        # error级别
        file_handler_error = TimedRotatingFileHandler(
            filename=self.logs_dir + os.sep + 'Error-{}.log'.format(self.now_time),  # 定义日志的存储
            when='MIDNIGHT',
            backupCount=1,  # 最多存放日志的数量
            encoding="UTF-8",  # 使用UTF - 8的编码来写日志
        )
        file_handler_error.setLevel(logging.ERROR)  # 设置日志级别
        file_handler_error.setFormatter(self.log_formatter)  # 设置日志格式
        log_logger.addHandler(file_handler_error)

        return log_logger


logger = GetLogger().get_logger()
