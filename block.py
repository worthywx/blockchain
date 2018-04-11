# --*-- coding: utf-8 --*--
"""
Author  : Worthy
File    : block.py
Time    : 2018/4/10 下午12:53
"""

import datetime
import hashlib


class Block(object):
    """
    区块类
    """
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
        return sha.hexdigest()


def create_genesis_block():
    """生成创世区块"""
    return Block(0, datetime.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
    """计算下一个区块"""
    index = last_block.index + 1
    timestamp = datetime.datetime.now()
    previous_hash = last_block.hash
    data = "Block " + str(index)
    return Block(index, timestamp, data, previous_hash)
