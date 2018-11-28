#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/2 15:10
# @Author  : KelvinYe
#
# 获取配置属性值
#
import os
import configparser

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           os.pardir, os.pardir, 'resources', 'config.ini'))


def get(section, key, filepath=CONFIG_PATH):
    """获取配置文件中的属性值，默认读取config.ini。

    Args:
        section: section名
        key: 属性名
        filepath: 配置文件路径

    Returns:
        属性值
    """
    if not os.path.exists(filepath):
        raise FileExistsError(filepath + ' 配置文件不存在')
    config = configparser.ConfigParser()
    config.read(filepath)
    return config.get(section, key)


def get_project_path():
    """返回项目根目录路径。
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))


def get_resources_path():
    """返回项目资源目录路径。
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'resources'))


if __name__ == '__main__':
    print(CONFIG_PATH)
    print(get_project_path())
    print(get_resources_path())
