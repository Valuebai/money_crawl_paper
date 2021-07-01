#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
"""
整个过程基本分为以下几个步骤，也是该脚本的主体思路

1. 获取需要改变编码格式的文件夹路径
2. 读取该文件夹下的txt文件，利用第三方库chardet预测编码，并将该编码格式记录
3. 将该txt文件按预测的编码格式解码后，用utf8重新编码，重新写入源文件并覆盖，实现转码
4. 对每一个文件重复2-3步骤，直到所有的txt都被重新编码

１． 由于事先所接收的文件编码格式多且杂乱，所以需要通过chardet预测，如预测出现问题则可能导致解码错误，重新写入时会出现乱码现象，至今未曾解决，但该bug出现频率不高，常见于文本量极小的中文文件。
２． chardet 不能精确到gb2312，所以预测结果为gb2312时，需要将其归为GBK，gb2312也确实属于GBK的子集。
３． 预测结果为utf8的文本直接不作处理
４．主体思路应该为对单个文件的预测，解码，重新编码
"""
import codecs
import chardet


# 检验文本文件的编码格式并转为utf-8
def txt_format_2_utf8(filename, out_enc="UTF-8"):
    try:
        content = open(filename, 'rb').read()
        source_encoding = chardet.detect(content)
        print("*************************")
        print(f'file={filename}')
        print("编码格式: " + source_encoding['encoding'])

        if source_encoding['encoding'] != "utf-8":
            if source_encoding['encoding'] == 'GB2312':
                content = content.decode("GBK")
                content = content.encode(out_enc)
                codecs.open(filename, 'wb').write(content)
            else:
                content = content.decode(source_encoding['encoding']).encode(out_enc)
                codecs.open(filename, 'wb').write(content)
            print("转换完成")
            print("*************************")
        else:
            print("无需转换")
            print("*************************")

    except IOError as err:
        print("I/O error:{0}".format(err))


if __name__ == "__main__":
    print('abc')
    txt_format_2_utf8(filename='/Users/luhb9/myCode/codeZhou/zhou_pyqt/data/txt_format_test/“巴黎贝甜”在中国的营销策略分析的副本.txt')
    txt_format_2_utf8(filename='/Users/luhb9/myCode/codeZhou/zhou_pyqt/data/txt_format_test/《英雄联盟》用户体验调查分析的副本.txt')
