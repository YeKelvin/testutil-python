#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/14 09:13
# @Author  : Kelvin.Ye
from _datetime import datetime
from time import time


def current_time_as_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def current_time_as_dirname():
    return datetime.now().strftime('%Y.%m.%d %H.%M.%S')


def current_time_as_ms():
    """获取毫秒级时间戳，用于计算毫秒级耗时
    """
    return int(time() * 1000)


def current_time_as_s():
    """获取秒级时间戳，用于计算秒级耗时
    """
    return int(time())


def seconds_convert_to_hms(seconds: int) -> str:
    """秒数转换为时分秒

    Args:
        seconds: 秒数

    Returns: 时分秒

    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%02dh:%02dm:%02ds' % (h, m, s)
