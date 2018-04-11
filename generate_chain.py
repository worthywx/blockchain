# --*-- coding: utf-8 --*--
"""
Author  : Worthy
File    : generate_chain.py
Time    : 2018/4/10 下午1:38
"""

from block import *

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

BLOCKS_NUM = 20

for i in range(BLOCKS_NUM):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add

    print "Block #{} has been added to the blockchain!".format(block_to_add.index)
    print "Hash: {}".format(block_to_add.hash)