#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
import json
import os
import time
import pandas as pd
from common.log import logger
import xlsxwriter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_OUTPUTS = BASE_DIR + '/outputs/'


def save_json_to_excel(json_data):
    """
    读取json数据并存到xlxs中
    json_data: 数据格式为：[{'学校':'XX大学', '标题':'AAAA'},{'学校':'XX大学', '标题':'AAAA'},...]

    """
    # 获取当前时间
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

    # 读取json数据并存到xlxs中
    try:
        df = pd.read_json(json.dumps(json_data), encoding='UTF-8')  # 这里的json/dict的key就默认是第一行的表头，key可以用中文
        # openpyxl.utils.exceptions.IllegalCharacterError 错误原因分析及解决办法
        # 新增了下面的engine='xlsxwriter' ， 需要pip install xlsxwriter
        df.to_excel(r'all_results_{}.xlsx'.format(current_time), index=False, engine='xlsxwriter')  # 不要索引
        logger.info('save_json_to_excel成功')
    except Exception as e:
        logger.error(f'save_json_to_excel失败：{e}')


def save_json_to_excel_with_name(save_name, json_data):
    """
    读取json数据并存到xlxs中
    json_data: 数据格式为：[{'学校':'XX大学', '标题':'AAAA'},{'学校':'XX大学', '标题':'AAAA'},...]
    因为pandas需要读取绝对路径，所有这里只给名称即可
    """

    # openpyxl.utils.exceptions.IllegalCharacterError 错误原因分析及解决办法
    # 新增了下面的engine='xlsxwriter' ， 需要pip install xlsxwriter
    try:
        df = pd.read_json(json.dumps(json_data), encoding='UTF-8')  # 这里的json/dict的key就默认是第一行的表头，key可以用中文
        save_file_name = r'{}/{}.xlsx'.format(PATH_OUTPUTS, save_name)
        df.to_excel(save_file_name, index=False, engine='xlsxwriter')  # 不要索引
        logger.info(f'写入xls成功~{save_file_name}')
    except Exception as e:
        logger.error(f'save_json_to_excel失败：{e}')


def write_file(save_file_path, save_content):
    with open(save_file_path, 'w', encoding='utf-8') as f:
        logger.info(f'打开要写入保存的文件{save_file_path}')
        f.write(save_content)
    logger.info(f'成功写入文件：{save_file_path}')


def write_file_with_name(save_name, save_content):
    """write json"""
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    final_save_name = './outputs/wf_{}_all_id_{}.txt'.format(save_name, current_time)
    with open(final_save_name, 'w', encoding='utf-8') as f:
        f.write(save_content)
    logger.info(f'{final_save_name}文件写入完成')


# 定义读取图片函数,以'b'  binary mode二进制数据
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


# TODO 自己百度with open 的 r和 rb区别
def read_txt_file_content(txt_path):
    with open(txt_path, 'r', encoding='UTF-8') as f:
        return f.read()


def read_json(json_path):
    """Read json"""
    try:
        logger.info(f'json文件读取中...{json_path}')
        with open(json_path, 'r', encoding='UTF-8')as fp:
            json_data = json.load(fp)
            return json_data
    except Exception as e:
        logger.error(f'read_json报错={e}')


def write_json(dict_data):
    """write json
    默认保存到outputs文件夹中
    """
    # 获取当前时间
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    try:
        save_name = './outputs/data_json_{}.json'.format(current_time)
        with open(save_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(dict_data, ensure_ascii=False, indent=4))
        logger.info(f'json文件写入成功~{save_name}')
    except Exception as e:
        logger.error(f'write_json报错={e}')


def write_json_with_name(save_name, dict_data):
    """write json
    """
    # 获取当前时间
    # current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    try:
        with open(save_name, 'a+', encoding='utf-8') as f:
            f.write(json.dumps(dict_data, ensure_ascii=False, indent=4))
        logger.info(f'json文件写入成功{save_name}')
    except Exception as e:
        logger.error(f'write_json_with_name报错={e}')


def get_files_by_suffix(path, suffix_name):
    """
    获取指定路径下所有带有.xxx后缀名的文件
    Args:
        path: 指定的文件夹路径
        suffix_name: 固定格式，为 suffix_name=".apk"

    Returns: files of list

    """

    file_num = 0
    res = []
    # 遍历该文件夹
    # 默认先读取当前文件夹里面的文件，如果存在子文件夹，读完当前再遍历子文件夹里面的
    for root, dirs, files in os.walk(path):
        # logger.info(files)
        for file in files:  # 遍历刚获得的文件名files
            filename, extension = os.path.splitext(file)  # 将文件名拆分为文件名与后缀
            if extension == suffix_name:  # 判断该后缀是否为.X文件
                file_num = file_num + 1  # 文件个数标记
                # logger.info(file_num, os.path.join(root,filename)) #输出文件号以及对应的路径加文件名
                # res.append(filename)  # ["a","b"]格式，不带后缀名，需要自己拼接.apk后缀
                # res.append(filename + suffix_name)  # ["a.x","b,x"]格式
                res.append(root + '/' + filename + suffix_name)  # ["C:\\a.x"]格式
    logger.info("[file_tools]找到文件列表={}".format(res))
    if not res:
        logger.error("[file_tools]输入的路径不存在.{}文件！".format(suffix_name))
        return None
    else:
        return res


def get_folder_by_path(target_path):
    """
    获取指定路径下文件夹的名称
    Args:
        target_path: 指定的文件夹路径，如 path='./input/'，后面要加/

    Returns: files of list

    """

    res = []
    # 遍历该文件夹
    # 默认先读取当前文件夹里面的文件，如果存在子文件夹，读完当前再遍历子文件夹里面的
    for folder, dirs, files in os.walk(target_path):
        if folder != target_path:
            res.append(folder)

    return res


def get_folder_name_by_path(target_path):
    """
    获取指定路径下文件夹的名称
    Args:
        target_path: 指定的文件夹路径，如 path='./input/'，后面要加/

    Returns: files of list

    """

    res = []
    # 遍历该文件夹
    # 默认先读取当前文件夹里面的文件，如果存在子文件夹，读完当前再遍历子文件夹里面的
    for folder, dirs, files in os.walk(target_path):
        if folder != target_path:
            folder_name = folder.split('\\')[-1]
            if '.apk' in folder_name:
                res.append(folder_name)

    return res


if __name__ == "__main__":
    pass
    print(BASE_DIR)
    print(PATH_OUTPUTS)
