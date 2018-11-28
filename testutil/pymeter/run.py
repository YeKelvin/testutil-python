#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/1 10:09
# @Author  : KelvinYe
from fire import Fire

from pymeter.jmeter import run

"""
执行命令：  python run.py --env=${env} --path=${path}
说明：     {testEnv}必填，{path}选填，如path非空，则只执行path的脚本，否则执行regression-testing目录下所有脚本

env:      测试环境配置文件名（需后缀）
path:     指定需执行的脚本目录或脚本（相对路径，脚本需后缀）
"""
if __name__ == '__main__':
    Fire(run)
