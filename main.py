#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Software: PyCharm
# @Author  : https://github.com/namebai/
"""
# 在万方上搜索，将id复制出来，按照下面的格式定义要爬取的期刊的文章ID
# 搜索url：https://s.wanfangdata.com.cn/magazine?q=%E6%96%87%E5%AD%A6%E8%AF%84%E8%AE%BA
# 复制地方：https://www.wanfangdata.com.cn/sns/perio/wlxb (perio后面的)
"""
from api_wanfang.get_abstract import get_wf_one_periodical_all_abstract
from common.log import logger
from common.file_tools import save_json_to_excel_with_name, read_json

# 定义要爬取的期刊名称
# wf_periodical_list = {
#     'jssx': '计算数学',
#     'wgwxpl': '外国文学评论'
# }
wf_periodical_list = {
    'jssx': '计算数学',
    'wgwxpl': '外国文学评论',
    'wlxb': '物理学报',
    'gxxb': '光学学报',
    'zgjg': '中国激光',
    'wlxjz': '物理学进展',
    'gzxb': '光子学报',
    'wxpl': '文学评论',
    'wxyc': '文学遗产',
    'wgwxpl': '外国文学评论',
    'ddzjpl': '当代作家评论',
    'wgwxyj': '外国文学研究',
    'sxxb': '数学学报',
    'jssx': '计算数学',
    'yysxxb': '应用数学学报',
    'sxjz': '数学进展',
    'mhxtysx': '模糊系统与数学'
}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.info('begin...')
    # 拼接所有想要爬取的期刊id
    # 如果有某个期刊没有生成相应的json或excel，需要检查error日志，并注释掉上面成功的，重新跑失败的
    for periodical_id, periodical_name in wf_periodical_list.items():
        get_wf_one_periodical_all_abstract(periodical_id, periodical_name)

    aa = read_json('/Users/luhb9/myCode/codeZhou/crawl_wf_cnki_paper/outputs/wf_中国哲学史_zgzxs_data.json')
    save_json_to_excel_with_name('aaa', aa)
