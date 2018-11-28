#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/12 16:24
# @Author  : KelvinYe

import socket
import telnetlib


class Telnet:
    def __init__(self, host, port, encoding='GBK', finish_str='dubbo>', connect_timeout=10, read_timeout=10):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.finish_str = finish_str
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout

    def execute(self, command):
        # 初始化telnet
        try:
            telnet = telnetlib.Telnet(host=self.host, port=self.port, timeout=self.connect_timeout)
        except socket.error as err:
            print(f'[host:${self.host} port:${self.port}] ${err}')
            return

        # 触发doubble提示符
        telnet.write('\n')

        # 执行命令
        telnet.read_until(self.finish_str, timeout=self.read_timeout)
        telnet.write(f'${command}\n')

        # 获取结果
        data = ''
        while data.find(self.finish_str) == -1:
            data = telnet.read_very_eager()

        telnet.close()  # or write('exit\n')

        return data

    def invoke(self, interface_name, param):
        command = rf'invoke ${interface_name}(${param})'
        return self.execute(command)


if __name__ == '__main__':
    pass
