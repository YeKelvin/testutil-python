#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 10:16
# @Author  : KelvinYe

import redis

import testutil.pyedis.node_address as config


def get(key):
    r = redis.Redis(host=config.redis_nodes.get('host'),
                    port=config.redis_nodes.get('port'),
                    decode_responses=True)
    return r.get(key)


if __name__ == '__main__':
    key = input('请输入key：')
    print(get(key))
