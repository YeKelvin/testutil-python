#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 17:42
# @Author  : Kelvin.Ye

import os
import xml.etree.ElementTree as eltree
from datetime import datetime

from testutil import config, content_util
from testutil.content_util import replace
from testutil.file_util import make_zip
from testutil.path_util import get_script_list


class JMX:
    def __init__(self, jmx_path):
        self.jmx_path = jmx_path
        self.etree = eltree.parse(os.path.normpath(jmx_path))
        self.root = self.etree.getroot()
        self.test_plan = self.root[0][0]
        self.main_tree = self.root[0][1]

    def save(self):
        self.etree(self.jmx_path, encoding='UTF-8', xml_declaration=True)


def doc2unix(jmx_path):
    """转换文档格式为UNIX

    Args:
        jmx_path: 脚本路径

    Returns:

    """
    content_util.doc2unix(jmx_path)


def backup(workspace: str):
    backupdir = os.path.join(workspace, 'backup')
    regression_parent = os.path.join(workspace, 'regression-testing')
    version_parent = os.path.join(workspace, 'version-testing')
    regression_zipname = 'regression %s.zip' % datetime.now().strftime('%Y%m%d-%H%M%S')
    version_zipname = 'version %s.zip' % datetime.now().strftime('%Y%m%d-%H%M%S')
    make_zip(regression_parent, backupdir, regression_zipname)
    make_zip(version_parent, backupdir, version_zipname)


if __name__ == '__main__':
    workspace = os.path.normpath(config.get('jmeter', 'workspace'))
    backup(workspace)  # 先备份，打包为zip文件
    scrips = get_script_list(workspace)  # 获取脚本列表
    for jmx in scrips:
        replace(jmx, 'ExtentHtmlReportGui', 'LocalHtmlReportGui')
        replace(jmx, 'Extent Html Report', 'Local HTML Report')
        # 转换文档格式为UNIX
        content_util.doc2unix(jmx)
        print(f'{jmx} - 执行成功')
