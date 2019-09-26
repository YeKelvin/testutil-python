#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/6/1 10:09
# @Author  : Kelvin.Ye

import os
import sys
import traceback

# 添加项目路径到path
sys.path.append(os.path.dirname(sys.path[0]))
from subprocess import Popen, PIPE, STDOUT

from testutil import config
from testutil.number_util import decimal_to_percentage
from testutil.time_util import current_time_as_s, seconds_convert_to_hms, current_time_as_dirname
from testutil.path_util import (path_transform_reportname, get_script_list,
                                get_abspath_by_scriptname, isjmx,
                                get_abspath_by_relative_path, get_file_list_by_env)


class Jmeter:
    """Jmeter类
    """

    def __init__(self, jmeter_bin: str, env: str, reportname: str, is_append: str):
        self.jmeter_path = os.path.join(jmeter_bin, 'jmeter')
        self.options = (rf' -JconfigName="{env}" -JreportName="{reportname}" -JisAppend="{is_append}" '
                        rf'-JprintSampleResultToConsole="false" -n -t ')
        self.__command = self.jmeter_path + self.options

    def execute(self, jmx_abspath: str) -> None:
        """根据路径执行jmeter脚本

        Args:
            jmx_abspath: 脚本绝对路径

        Returns: None

        """
        command = self.__command + jmx_abspath
        print(f'Commond:[{command}]\n')
        popen = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, universal_newlines=True)
        while popen.poll() is None:  # 检查子进程是否结束
            line = popen.stdout.readline()
            line = line.strip()
            if line:
                print(line)
        if popen.returncode == 0:
            print('Script execution success.\n')
        else:
            print('Script execution failed.\n')


def run(env: str, path: str) -> None:
    jmeterbin = config.get('jmeter', 'bin')
    workspace = config.get('jmeter', 'workspace')
    reportname = 'regression-testing-report.html'
    is_append = 'true'
    regression_parent = os.path.join(workspace, 'regression-testing')
    currenttime = current_time_as_dirname()
    abspath = None
    jmx_list = []

    if path == "":
        # 如 path 为空，则执行 workspace/regression-testing回归目录 下所有jmx脚本
        jmx_list = get_script_list(regression_parent)
    else:
        # 如 path 非空，则先判断 path 是目录还是脚本
        abspath = get_abspath_by_relative_path(workspace, path)
        if os.path.isdir(abspath):
            reportname = path_transform_reportname(path)
            jmx_list = get_script_list(abspath)
        elif isjmx(abspath):
            reportname = os.path.split(abspath)[1][:-4]
            jmx_list.append(get_abspath_by_scriptname(workspace, path))
        else:
            print(f'" {workspace} "下，不存在 {abspath} 此目录或脚本')
            sys.exit()

    # 待执行脚本列表非空校验
    if len(jmx_list) == 0 or jmx_list[0] == '':
        print(f'" {workspace} "下，目录或脚本不存在')
        sys.exit()

    # 排除脚本名含 skip 的脚本
    del_skip_script(jmx_list)

    # 统计总脚本数
    script_number = len(jmx_list)
    # reportname = rf'[{reportname}]{currenttime}.html'
    reportname = rf'[{currenttime}]{reportname}.html'
    os.chdir(jmeterbin)  # 设置当前工作路径为jmeter\bin
    jmeter = Jmeter(jmeterbin, env, reportname, is_append)

    print(f'JmeterBin:[{jmeterbin}]')
    print(f'Workspace:[{workspace}]')
    print(f'脚本读取路径:[{abspath}]')
    print(f'总脚本数:[{script_number}]\n')

    # 用于统计完成脚本数
    completed_number = 0
    # 记录开始时间
    starttime = current_time_as_s()

    for script in jmx_list:
        current_starttime = current_time_as_s()
        jmeter.execute(script)
        current_elapsed_time = current_time_as_s() - current_starttime
        completed_number += 1
        print(f'当前脚本耗时:[{seconds_convert_to_hms(current_elapsed_time)}]')
        print(f'已完成脚本数:[{completed_number}]，剩余脚本数:[{script_number - completed_number}]，'
              f'当前总进度:[{decimal_to_percentage(completed_number / script_number)}]\n')

    # 统计总耗时
    total_elapsed_time = current_time_as_s() - starttime
    print(f'总耗时:[{seconds_convert_to_hms(total_elapsed_time)}]')
    reportpath = os.path.join(config.get('jmeter', 'home'), 'htmlreport', reportname)
    print(f'所有脚本执行完毕，详细数据请查看测试报告，报告路径:[{reportpath}]\n')


def del_skip_script(jmx_list: list):
    # 待删列表
    del_list = []

    # 查找脚本名含 skip 的脚本列表索引
    for index, jmx in enumerate(jmx_list):
        if 'skip' in jmx:
            del_list.append(index)

    # 根据待删列表删除元素
    for index in del_list:
        del jmx_list[index]


def get_env_list() -> list:
    """打印测试环境列表
    """
    config_path = os.path.join(config.get('jmeter', 'home'), 'config')
    return get_file_list_by_env(config_path)


if __name__ == '__main__':
    env_list = get_env_list()
    print(f'支持的测试环境: {env_list}')
    while True:
        env = input('请输入以上测试环境配置之一的名称：')
        if env in env_list:
            break
        print('不存在此测试环境配置，请重新输入。')
    path = input('请输入需执行的目录或脚本（相对路径，脚本需后缀）：')
    try:
        run(env, path)
    except Exception as e:
        traceback.print_exc()
    finally:
        input('按任意键退出')
