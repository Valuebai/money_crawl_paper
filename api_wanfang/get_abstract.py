#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
import json
import time

import requests

from common.file_tools import write_json_with_name, save_json_to_excel_with_name
from common.timestamp_convert import timeStamp_ms_convert_time
from common.log import logger


def get_periodical_one_year_all_abstract(journal_name, publishYear, year_batches):
    """
    获取《期刊》 XXX年一共有多少期多少文章，并获取摘要信息
    :param journal_name: 期刊代码，如汉语学习代码为：hanyxx
    :param publishYear: 出刊年份
    :return: []
    """
    logger.info(f'调用get_periodical_year_article()函数, 期刊={journal_name}, 年份={publishYear}')

    Info_URL = 'https://www.wanfangdata.com.cn/sns/third-web/per/perio/articleList'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    one_year_list = []
    # 从第1期到year_batches期
    for issueNum in range(1, year_batches + 1):
        # 获取每一期有XX页
        try:
            data_one = {
                "page": 1,
                "pageSize": 10,
                "perioId": journal_name,
                "publishYear": publishYear,
                "issueNum": issueNum,
            }

            session = requests.session()
            # logger.info(f'1请求url={Info_URL}, 请求数据={data_one}')
            res = session.post(Info_URL, data=data_one, headers=headers)
            data = res.content.decode()
            info = json.loads(data)
            # logger.info(f'1请求成功，返回数据={info}')
            pageTotal = info['pageTotal']
        except Exception as e:
            pageTotal = 10
            logger.error(f'1请求报错,url={Info_URL}，{e}')

        logger.info(f'共有{pageTotal}页')

        # 每一期有多少页
        for page_id in range(1, pageTotal + 1):

            data_two = {
                "page": page_id,
                "pageSize": 10,
                "perioId": journal_name,
                "publishYear": publishYear,
                "issueNum": issueNum,
            }
            try:
                session = requests.session()
                logger.info(f'2请求url={Info_URL}, 数据={data_two}')
                res = session.post(Info_URL, data=data_two, headers=headers)
                data = res.content.decode()
                info_data = json.loads(data)

                if not info_data['pageRow']:
                    logger.info('返回的json数据中的pageRow字段为空')
                    logger.error('返回的json数据中的pageRow字段为空')
                    continue
                else:
                    # 获取文章id

                    for info in info_data['pageRow']:
                        logger.info(f"2请求成功，返回数据=")
                        logger.info(info)

                        if info:
                            if '征稿简则' in info['Title'][0]:
                                continue
                            if '前言' in info['Title'][0]:
                                continue
                            if '征稿' in info['Title'][0]:
                                continue
                            # logger.info(f'摘要数据={info}')
                            # 英文标题
                            if len(info['Title']) > 1:
                                eng_title = info['Title'][1]
                            else:
                                eng_title = ''
                            if 'Abstract' in info:
                                # 中文摘要
                                if len(info['Abstract']) > 0:
                                    cn_abstract = info['Abstract'][0]
                                else:
                                    cn_abstract = ''
                                # 英文摘要
                                if len(info['Abstract']) > 1:
                                    eng_abstract = info['Abstract'][1]
                                else:
                                    eng_abstract = ''
                            else:
                                cn_abstract = ''
                                eng_abstract = ''
                            # Fund
                            if 'Fund' in info:
                                fund = info['Fund']
                            else:
                                fund = ''
                            # Volum
                            if 'Volum' in info:
                                volum = info['Volum']
                            else:
                                volum = ' '
                            # Keywords
                            if 'Keywords' in info:
                                Keywords = info['Keywords']
                            else:
                                Keywords = ' '
                            # Creator
                            if 'Creator' in info:
                                Creator = info['Creator']
                            else:
                                Creator = ' '
                            # AuthorOrg
                            if 'AuthorOrg' in info:
                                AuthorOrg = info['AuthorOrg']
                            else:
                                AuthorOrg = ' '
                            # SequenceInIssue
                            if 'SequenceInIssue' in info:
                                SequenceInIssue = info['SequenceInIssue']
                            else:
                                SequenceInIssue = ' '
                            # MetadataOnlineDate
                            if 'MetadataOnlineDate' in info:
                                MetadataOnlineDate = info['MetadataOnlineDate']
                                MetadataOnlineDate = timeStamp_ms_convert_time(MetadataOnlineDate)
                                MetadataOnlineDate = MetadataOnlineDate.split(' ')[0]
                            else:
                                MetadataOnlineDate = ''

                            # 拼接数据
                            one_article_info = {
                                "期刊": info['PeriodicalTitle'][0],
                                "文章Id": info['Id'],
                                "中文标题": info['Title'][0],
                                "英文标题": eng_title,
                                "中文摘要": cn_abstract,
                                "英文摘要": eng_abstract,
                                "中文关键词": Keywords,

                                "作者": Creator,
                                "作者单位": AuthorOrg,
                                "期刊ID": info['PeriodicalId'],
                                "年，卷(期)": str(info['PublishYear']) + ' ' + str(volum) + '(' + str(
                                    SequenceInIssue) + ')',

                                "基金项目": fund,
                                "在线发布时间": MetadataOnlineDate,
                                "原文链接": Info_URL.split('://')[-1] + info['Id']
                            }
                            one_year_list.append(one_article_info)

            except Exception as e:
                logger.error(f'2请求报错,url={Info_URL}，{e}')
                logger.error(info)

    return one_year_list


def get_wf_one_periodical_all_abstract(wf_periodical_id, wf_periodical_name):
    """
    获取万方上一个期刊的所有摘要信息，并存储到json和excel中
    :param wf_periodical_id: 期刊id
    :param wf_periodical_name: 期刊名称
    :return: None
    """
    logger.info(f'期刊名称={wf_periodical_name}, id={wf_periodical_id}，获取该期刊所有文章的摘要中...')

    # 根据请求URL获取该期刊有多少年，每一年有多少期
    URL = 'https://www.wanfangdata.com.cn/sns/third-web/per/perio/snsYearTree'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    try:
        data_year = {
            "perioId": wf_periodical_id
        }
        session = requests.session()
        logger.info(f'请求url={URL}, data={data_year}')
        res = session.post(URL, data=data_year, headers=headers)
        data = res.content.decode()
        json_info = json.loads(data)
        # logger.info(f'请求成功，返回数据={json_info}')
        if not json_info['formalPublishes']:
            logger.info('返回的json数据中的formalPublishes字段为空')
            logger.error('返回的json数据中的formalPublishes字段为空')
        else:
            # 字段有数据，遍历年份
            wf_one_periodical_all_abstract_list = []
            for info in json_info['formalPublishes']:
                # 获取年份
                year = info['name']
                # 获取这一年有多少期
                year_batches = len(info['perioBatches'])
                logger.info(f'获取{year}年《{wf_periodical_name}》期刊(共{year_batches}期)的所有摘要...')
                # 逐年获取摘要信息
                one_year_abstract = get_periodical_one_year_all_abstract(wf_periodical_id, year, year_batches)
                # 将每一期每一年的摘要数据[{}{}]更新到期刊总结果上
                wf_one_periodical_all_abstract_list.extend(one_year_abstract)

                logger.info(f'{year}年《{wf_periodical_name}》期刊的所有摘要信息={one_year_abstract}')
            # end for
            logger.info(f'《{wf_periodical_name}》期刊最近20年的所有文章摘要={wf_one_periodical_all_abstract_list}')

            # 将该期刊的数据写入到json中，默认保存到outputs文件夹中
            final_save_name = './outputs/wf_{}_{}_data.json'.format(wf_periodical_name, wf_periodical_id)
            write_json_with_name(final_save_name, wf_one_periodical_all_abstract_list)

            # 将数据转为excel, 这里只有传保存的名称就行
            save_name = wf_periodical_name + '_abstract_' + wf_periodical_id
            save_json_to_excel_with_name(save_name, wf_one_periodical_all_abstract_list)

    except Exception as e:
        logger.error(f'请求报错,url={URL}，{e}')
        logger.error(f'期刊名称={wf_periodical_name}, id={wf_periodical_id},获取该期刊数据转为json和excel失败，请重试')


if __name__ == '__main__':
    a = []
    b = [{'aa': 'aaa'}, {'bb': 'bbb'}]
    a.extend(b)
    c = [{'aa1': 'aaa'}, {'bb2': 'bbb'}]
    a.extend(c)
    c = [{'aa1': 'aaa111'}, {'bb2': 'bbb222'}]
    a.extend(c)
    print(a)
    print(timeStamp_ms_convert_time(1592409600000))
