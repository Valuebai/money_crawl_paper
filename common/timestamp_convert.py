#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2020/7/23 18:03
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
"""
    <moudule>.$ {NAME} 
    ~~~~~~~~~~~~~~~

    常用的秒，毫秒时间转换

    Usage Example
    -------------
    ::
"""
import time


def timeStamp_ms_convert_time(time_num):
    """
    输入毫秒级时间戳的时间，转出正常格式的时间
    如: 1590813969846 -> 2020-05-30 12:46:09
    param time_num: ms时间戳
    return: 正常格式的时间
    """
    time_stamp = float(time_num / 1000)
    time_array = time.localtime(time_stamp)
    normal_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    # print(normal_time)

    return normal_time


def timeStamp_s_convert_time(time_num):
    """
    输入秒级时间戳的时间，转出正常格式的时间
    如: 1595498910 -> 2020-07-23 18:08:30
    param time_num: ms时间戳
    return: 正常格式的时间
    """
    time_array = time.localtime(int(time_num))
    normal_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    # print(normal_time)

    return normal_time


def main():
    """主函数"""
    print('test')
    print(timeStamp_s_convert_time(1595498910))


if __name__ == "__main__":
    main()
