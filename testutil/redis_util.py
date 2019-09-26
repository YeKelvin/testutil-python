#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 10:16
# @Author  : Kelvin.Ye

import sys

import redis
from rediscluster import StrictRedisCluster

from testutil import config


class Redis:
    @staticmethod
    def get(key: str):
        r = redis.Redis(host=config.get('redis', 'host'),
                        port=config.get('redis', 'port'),
                        decode_responses=True)
        return r.get(key)


class RedisCluster:
    @staticmethod
    def get(key: str):
        try:
            rc = StrictRedisCluster(startup_nodes=config.get('redis_cluster', 'test_new_sh'))
        except Exception:
            print('Connect Error!')
            sys.exit(1)
        return rc.get(key)


if __name__ == '__main__':
    key = input('请输入key：')
    print(Redis.get(key))
