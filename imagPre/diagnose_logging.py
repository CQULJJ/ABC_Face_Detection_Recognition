# -*- coding: utf-8 -*-
# @Time    : 2019/7/5 10:52
# @Author  : LiJinjin
# @Email   : 1484972292@qq.com
# @File    : diagnose_logging.py
# @Software: PyCharm

# coding:utf-8
#
# 日志类
# diagnose_logging
#
# 定义日志记录格式
#
# ==============================================================================

import logging


class Logger():
    def __init__(self, logName):
        # 创建一个logger
        self.logger = logging.getLogger(logName)

        # 判断，如果logger.handlers列表为空，则添加，否则，直接去写日志,试图解决日志重复
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            # 创建一个handler，用于写入日志文件
            fh = logging.FileHandler('log.log')
            fh.setLevel(logging.INFO)

            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # 定义handler的输出格式
            formatter = logging.Formatter('%(levelname)s:%(asctime)s -%(name)s -%(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler处理器
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

    '''
    调用办法：
    #引入
    from img_logging import Logger
    #文件名
    log = Logger('abc.py')
    logger = log.getlog()
    #提示信息格式一
    logger.info('main')


    '''