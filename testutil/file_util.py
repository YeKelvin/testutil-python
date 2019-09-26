#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/7 14:55
# @Author  : Kelvin.Ye
#
# 文件操作
#
import os
import zipfile

from common.logger import get_logger

log = get_logger(__name__)


def make_zip(source_dir, output_dir, zipname):
    """备份文件，打包目录下所有文件为zip包

    Args:
        source_dir: 目标目录路径
        output_dir: 打包输出路径
        zipname:    zip包名称

    Returns:

    """
    zipf = zipfile.ZipFile(os.path.join(output_dir, zipname), 'w', zipfile.ZIP_DEFLATED)
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            abspath = os.path.join(parent, filename)
            arcname = abspath[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(abspath, arcname)
    zipf.close()
    log.info('文件备份成功')
