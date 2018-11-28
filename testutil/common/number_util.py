#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 17:10
# @Author  : KelvinYe


def decimal_to_percentage(decimal: float) -> str:
    """小数转百分比

    Args:
        decimal: 小数

    Returns: 百分比值

    """
    return '%.2f%%' % (decimal * 100)
