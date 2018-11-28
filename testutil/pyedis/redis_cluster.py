#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 10:17
# @Author  : KelvinYe
import sys

from rediscluster import StrictRedisCluster

import testutil.pyedis.node_address as config


def get(key):
    try:
        rc = StrictRedisCluster(startup_nodes=config.redis_cluster_nodes.get('test_new_sh'))
    except Exception:
        print('Connect Error!')
        sys.exit(1)
    return rc.get(key)


if __name__ == '__main__':
    key = input('请输入key：')
    print(get(key))
