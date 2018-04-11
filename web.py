# --*-- coding: utf-8 --*--
"""
Author  : Worthy
File    : web.py
Time    : 2018/4/10 下午1:56
"""
import datetime
import json

import requests
from flask import Flask, request

from block import Block
from generate_chain import blockchain

node = Flask(__name__)

# 存储节点交易记录
node_transactions = []

# 节点URL
peer_nodes = []

mining = True


@node.route('/transaction', methods=['POST'])
def transaction():
    if request.method == "POST":
        new_trans = request.get_json()

        node_transactions.append(new_trans)

        print "New transaction"
        print "FROM:{}".format(new_trans['from'])
        print "TO:{}".format(new_trans['to'])
        print "AMOUNT:{}\n".format(new_trans['amount'])

        return "Transaction submission successful\n"


miner_address = "sldjfwpw-sdflsjdf-sdfshglfhg-igwrhubxf"


def proof_of_work(last_proof):
    incrementor = last_proof + 1

    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1

    return incrementor


@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']

    proof = proof_of_work(last_proof)

    node_transactions.append({
        "from": "network",
        "to": miner_address,
        "amount": 1
    })

    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(node_transactions)
    }

    new_block_index = last_block.index + 1
    new_block_timestamp = datetime.datetime.now()
    last_block_hash = last_block.hash

    node_transactions[:] = []

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    blockchain.append(mined_block)

    return json.dumps({
        "index": new_block_index,
        "timestamp": new_block_timestamp,
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = []

    for block in blockchain:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
        chain_to_send.append(block)

    return json.dumps(chain_to_send)


def find_new_chains():
    """
    获取其他节点保存的区块链
    :return:
    """
    other_chains = []

    for node_url in peer_nodes:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)

    return other_chains


def consensus():
    """
    更新节点的区块链
    :return:
    """
    other_chains = find_new_chains()

    global blockchain
    longest_chain = blockchain

    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain

    blockchain = longest_chain


node.run(debug=True, port=5001)
