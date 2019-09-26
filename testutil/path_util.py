#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 17:45
# @Author  : Kelvin.Ye
#
# 路径处理
#
import os


def get_script_list(dirpath):
    """
    返回目录及子目录下所有的jmx脚本
    """
    jmxs = []
    for parent, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if filename.endswith('jmx'):
                jmxs.append(os.path.join(parent, filename))
    return jmxs


def get_abspath_by_scriptname(dirpath, scriptname):
    """
    返回指定脚本名的绝对路径
    """
    abspath = ''
    for parent, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if scriptname == filename:
                abspath = os.path.join(parent, filename)
                break
    return abspath


def get_abspath_by_keywords(dirpath, keywords):
    """
    根据keywords模糊搜索，返回第一个匹配成功的脚本的绝对路径，
    """
    abspath = ''
    for parent, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if keywords in filename:
                abspath = os.path.join(parent, filename)
                break
    return abspath


def get_abspath_by_relative_path(dirpath, relative_path: str):
    """
    根据 尾部部分路径 模糊搜索，返回第一个匹配成功的尾部相对路径的绝对路径
    """
    if relative_path.endswith('/') or relative_path.endswith('\\'):
        relative_path = relative_path[:-1]
    relative_path = os.path.normpath(relative_path)
    abspath = ''
    for parent, dirnames, filenames in os.walk(dirpath):
        for dirname in dirnames:
            if os.path.join(parent, dirname).endswith(relative_path):
                abspath = os.path.join(parent, dirname)
                break
        for filename in filenames:
            if os.path.join(parent, filename).endswith(relative_path):
                abspath = os.path.join(parent, filename)
                break
    return abspath


def isjmx(filename):
    """
    根据文件名（入参含后缀）判断文件后缀是否为 .xml
    """
    return os.path.splitext(filename)[-1] == '.jmx' if True else False


def isdir(dirname):
    """
    判断是否目录
    """
    return os.path.isdir(dirname)


def path_join(parent, child):
    """
    根据当前系统转换路径分隔符且合并路径
    """
    # 将String型路径的分隔符转换为当前系统的路径分隔符
    parent = os.path.normpath(parent)
    child = os.path.normpath(child)

    # 判断path入参第一个字符是否为路径分隔符（“/”，“\”），是则去掉，提高容错性
    if child[0] == os.path.sep:
        child = child[1:]
    return os.path.join(parent, child)


def path_transform_reportname(path: str):
    """
    根据路径转换为测试报告名称
    """
    # 因path值为人工输入，故不使用os.path.sep
    if path[0] == '/' or path[0] == '\\':
        path = path[1:]
    return path.replace('/', '.').replace('\\', '.')


def get_file_list_by_env(dirpath):
    env_list = []
    for file in os.listdir(dirpath):
        if file.endswith('.env'):
            env_list.append(file)
    return env_list
