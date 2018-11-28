#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 17:27
# @Author  : KelvinYe
import os
import re
import shutil
from enum import Enum

from common import config
from common.time_util import current_time_as_str
from file_io.file_util import make_zip
from testutil.common.logger import get_logger

"""
版本目录命令规则：
|-- VersionTesting/
    |-- yyyy年/
    |-- yyyy年/
        |-- 版本上线日期mmdd/
        |-- 版本上线日期mmdd/
            |-- 工单名.jmx
            |-- 应用名.类名.方法名.jmx

应用名枚举 = core | product | cbs | cdp | ass

回归目录命令规则：
|-- RegressionTesting/
    |-- 应用名A/
    |-- 应用名B/
        |-- 类名A/
        |-- 类名B/
            |-- 类名B.方法名A.版本上线日期yyyymmdd.jmx
            |-- 类名B.方法名B.版本上线日期yyyymmdd.jmx
"""

log = get_logger(__name__)


def script_sync(version_parent, regression_parent, startwith):
    """VersionTesting版本目录下脚本一键同步至RegressionTesting回归目录下

    Args:
        version_parent:    版本目录路径
        regression_parent: 回归目录径路
        startwith:         同步版本开始目录

    Returns:

    """
    scripts = get_script_abspath_list(version_parent, startwith)
    sorted(scripts, key=lambda i: i['version'])  # 排序
    for script in scripts:
        if is_interface_name(script['name']):
            # 如脚本名为接口名才执行同步操作
            log.debug(f'当前脚本={script["path"]}')

            # 获取当前脚本所属的回归目录路径
            current_regression_dir = scriptname_transform_regressionpath(script['name'], regression_parent)
            log.debug(f'回归目录={current_regression_dir}')

            # 获取当前脚本所属的回归目录中已存在的脚本路径
            regression_existed_script_path = get_existed_script_by_keywords(current_regression_dir,
                                                                            get_interface_name(script['name']))
            log.debug(f'回归目录下已存在的脚本={regression_existed_script_path}')
            if regression_existed_script_path:
                # 如回归目录已存在脚本，则根据规则覆盖脚本
                overwritefile(script['path'], regression_existed_script_path, script['version'])
            else:
                # 回归目录无则直接根据规则复制脚本
                copyfilewithversion(script['path'], current_regression_dir, script['version'])
    log.info('同步完成')


def get_script_abspath_list(dirpath, startwith):
    """从版本目录下递归返回所有的jmx脚本（带路径和版本号）

    Args:
        dirpath:   版本目录
        startwith: 开始版本号，大于等于版本号才返回

    Returns:
        {'name':'脚本名', 'path':'脚本绝对路径', 'version':'脚本所属版本号'} 的list
    """
    scripts = []
    for parent, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if filename.endswith('.jmx'):
                # 获取脚本绝对路径
                script_abspath = os.path.join(parent, filename)
                # 从路径中提取版本号
                version = get_version_in_versiondir(script_abspath)
                # 判断 脚本当前版本号 是否大于等于 需同步的版本号
                if version >= startwith:
                    scripts.append({'name': filename, 'path': script_abspath, 'version': version})
    return scripts


def is_interface_name(scriptname):
    """判断文件名是否为接口名

    Args:
        scriptname: jmeter脚本路径（含.jmx后缀）

    Returns:
        True | False
    """
    pattern = re.compile(r'[a-zA-z]+[.][a-zA-z]+[.][a-zA-z]+.jmx')
    m = pattern.match(scriptname)
    if m and scriptname == m.group():
        return True
    return False


def get_interface_name(name):
    """针对格式为 appname.classname.methodname.jmx 的文件返回真正的接口名

    Args:
        name: 脚本名（不含路径）

    Returns:
        真正的接口名
    """
    name = name[:-4]  # 去掉后缀
    names = name.split('.')
    return f'{names[1]}.{names[2]}'


def copyfile(source_file, output_file):
    """复制文件

    Args:
        source_file: 需要复制的文件路径
        output_file: 目标文件路径

    Returns:

    """
    shutil.copyfile(source_file, output_file)


def copyfilewithversion(source_file, output_dir, version):
    """复制文件，文件名带版本号（newdir目录不存在则创建）

    Args:
        source_file: 要复制的文件路径
        output_dir:  目标路径
        version:     版本号

    Returns:

    """
    log.debug('执行动作=复制脚本')
    names = os.path.split(source_file)[-1][:-4].split('.')  # 提取文件名
    scriptname = f'{names[1]}.{names[2]}.{version}.jmx'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    newfile = os.path.join(output_dir, scriptname)
    shutil.copyfile(source_file, newfile)


def overwritefile(source_file, existed_file, version):
    """覆盖文件，并更新覆盖文件的版本号

    Args:
        source_file:  需要复制的文件路径
        existed_file: 需要覆盖的文件路径
        version:      版本号

    Returns:

    """
    log.debug('执行动作=覆盖脚本')
    existedfilename = os.path.split(existed_file)[-1][:-4]  # [-1]表示截取path路径中的文件名，[:-4]表示去掉.jmx文件后缀
    current_version = existedfilename.split('.')[-1]  # 提取已存在脚本版本号
    if version > current_version:
        # 如 版本目录下脚本的版本号 大于 回归目录下同名脚本的版本号 则覆盖此脚本
        newdir = os.path.dirname(existed_file)
        os.remove(existed_file)
        copyfilewithversion(source_file, newdir, version)


def scriptname_transform_regressionpath(scriptname, regression_parent):
    """符合规则的脚本名 转换为 所属回归目录路径

    Args:
        scriptname:        脚本名（不含目录）
        regression_parent: 回归根目录路径

    Returns:
        脚本所属的回归目录路径
    """
    names = scriptname[:-4].split('.')  # 提取文件名
    appname, classname = names[0], names[1]
    return os.path.join(regression_parent, AppName.get_name(appname), classname)


class AppName(Enum):
    """应用名枚举类
    """
    core = 'cif-core'
    product = 'cif-product'
    cbs = 'cif-basic-service'
    cdp = 'cif-data-process'
    ass = 'cif-assistant'
    cc = 'certify--core'
    cds = ' cif-data-sync'
    cmb = ' cif-mappingback'

    @staticmethod
    def get_name(appname):
        """根据应用名简称获取应用全名
        """
        appfullname = None
        for app in AppName:
            if appname == app.name:
                appfullname = app.value
        return appfullname


def get_existed_script_by_keywords(dirpath, keywords):
    """根据keywords判断文件是否存在于rootdir目录下，存在则返回文件路径

    Args:
        dirpath:  根目录路径
        keywords: 关键词

    Returns:
        已存在脚本的路径 | None
    """
    for parent, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            if keywords in filename:
                return os.path.join(parent, filename)
    return None


def is_existed_version(dirpath, version):
    """判断是否存在该版本号的目录

    Args:
        dirpath: 目录路径
        version: 版本号

    Returns:
        True | False
    """
    year = version[:4]
    month = version[4:]
    return os.path.exists(os.path.join(dirpath, year, month))


def get_version_in_versiondir(abspath):
    """解析 VersionTesting 目录下的文件路径，获取版本号

    Args:
        abspath: 脚本绝对路径

    Returns:
        版本号
    """
    dirnames = os.path.dirname(abspath).split(os.sep)
    year_index = None
    month_index = None
    for i, name in enumerate(dirnames):
        if name == 'VersionTesting':
            year_index = i + 1
            month_index = i + 2
    return dirnames[year_index] + dirnames[month_index]


if __name__ == '__main__':
    workspace = config.get('jmeter', 'workspace')
    version_parent = os.path.join(workspace, 'VersionTesting')
    regression_parent = os.path.join(workspace, 'RegressionTesting')
    backupdir = os.path.join(workspace, 'backup')

    startwith = input('请输入需要开始同步的版本号：')
    while not is_existed_version(version_parent, startwith):
        startwith = input('无此版本，请重新输入正确的版本号：')

    zipname = 'regression-testing %s.zip' % current_time_as_str()
    # 备份回归目录
    make_zip(regression_parent, backupdir, zipname)
    # 开始同步脚本至回归目录
    script_sync(version_parent, regression_parent, startwith)
    input('按任意键退出')
