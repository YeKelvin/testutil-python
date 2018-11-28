#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/29 10:09
# @Author  : KelvinYe
#
# 文件内容增删改查
#
import os


def replace(file: str, oldstr: str, newstr: str):
    """替换匹配成功的文件内容

    Args:
        file: 文件路径
        oldstr: 需要替换的值
        newstr: 替换的值

    Returns:

    """
    with open(file, 'r', encoding='utf-8') as f_r, open(f'{file}.bak', 'w', encoding='utf-8') as f_w:
        for line in f_r:
            if oldstr in line:
                line = line.replace(oldstr, newstr)
            f_w.write(line)
    os.remove(file)
    os.rename(f'{file}.bak', file)


def delete(file: str, key: str):
    """删除匹配成功的文件内容

    Args:
        file: 文件路径
        key: 需要删除的值

    Returns:

    """
    with open(file, 'r', encoding='utf-8') as f_r, open(f'{file}.bak', 'w', encoding='utf-8') as f_w:
        for line in f_r:
            if key in line:
                line = line.replace(key, '')
            f_w.write(line)
    os.remove(file)
    os.rename(f'{file}.bak', file)


def delete_line(file: str, key: str):
    """删除匹配成功的行

    Args:
        file: 文件路径
        key: 需要删除的行或所在行的部分值

    Returns:

    """
    with open(file, 'r', encoding='utf-8') as f_r, open(f'{file}.bak', 'w', encoding='utf-8') as f_w:
        for line in f_r:
            if key not in line:
                f_w.write(line)
    os.remove(file)
    os.rename(f'{file}.bak', file)


def insert(file: str, key: str, direction: str, newstr: str):
    """新增内容

    Args:
        file: 文件路径
        key: 需要新增内容的位置的值
        direction: before（向前新增） | after（向后新增）
        newstr: 新增的值

    Returns:

    """
    with open(file, 'r', encoding='utf-8') as f_r, open(f'{file}.bak', 'w', encoding='utf-8') as f_w:
        for line in f_r:
            f_w.write(newstr)
            f_w.writelines(line)
            # todo


def doc2unix(file: str):
    """文件转为unix格式

    Args:
        file: 文件路径

    Returns:

    """
    with open(file, 'r', encoding='utf-8') as f_r, open(f'{file}.bak', 'w', encoding='utf-8', newline='\n') as f_w:
        for line in f_r:
            f_w.writelines(line)
    os.remove(file)
    os.rename(f'{file}.bak', file)


def new_line(file: str, prefix_str: str, newline_str: str):
    """新增一行内容

    Args:
        file: 文件路径
        prefix_str: 定位需要新增内容所在行的前一行内容
        newline_str: 新增行内容

    Returns:

    """
    with open(file, 'r', encoding='utf-8') as f_r, open(f'{file}.bak', 'w', encoding='utf-8') as f_w:
        for line in f_r:
            f_w.write(line)
            if prefix_str in line:
                f_w.writelines(newline_str)
    os.remove(file)
    os.rename(f'{file}.bak', file)


if __name__ == '__main__':
    pass
