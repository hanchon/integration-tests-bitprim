#!/usr/bin/env python3

# This file is just an example of a test that always fails to demonstrate how the runner.py works
# TODO: remove this file

from bitprim_utils.node import BitprimNode
from bitprim_utils.util import (
    sync_chain,
    assert_equal,
)
import time

if __name__ == "__main__":

    node1 = BitprimNode("../config/bch/cfg1", "./bn")
    node1.start()

    node2 = BitprimNode("../config/bch/cfg2", "./bn")
    node2.start()

    time.sleep(20)

    res, value = node1.rpc.get_info()
    if res:
        print("Node 1 get info:")
        print(value)
    else:
        print("Node 1 rpc call for get_info error")

    res, value = node2.rpc.get_info()
    if res:
        print("Node 2 get info:")
        print(value)
    else:
        print("Node 2 rpc call for get_info error")

    print("Node 1 best hash:")
    print(node1.rpc.generate_best_block_hash())
    print("Node 2 best hash:")
    print(node2.rpc.generate_best_block_hash())

    sync_chain([node1, node2])

    assert_equal(1, 2)

    node1.stop()
    node2.stop()

    node1.clean_files()
    node2.clean_files()
