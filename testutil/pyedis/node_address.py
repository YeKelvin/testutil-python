#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/12 14:21
# @Author  : KelvinYe

__test_new_sh = [{'host': '0.0.0.0', 'port': 0}]

__test_46_sh = [{'host': '0.0.0.0', 'port': 0}]

# redis集群节点
redis_cluster_nodes = {'test_new_sh': __test_new_sh,
                       'test_46_sh':  __test_46_sh}

# redis单节点 host and port
redis_nodes = {'test_new_sh': {'host': '', 'port': 6379}}
