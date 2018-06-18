from bitprim_utils.node import BitprimNode
from bitprim_utils.rpc import BitprimRPC

import time

if __name__ == "__main__":

    rpcport_node1 = 18332
    rpcport_node2 = 18335

    node1 = BitprimNode(1, rpcport_node1, "../config/bch/cfg", "./bn")
    node1.start()

    node2 = BitprimNode(2, rpcport_node2, "../config/bch/cfg", "./bn")
    node2.start()

    time.sleep(10)

    node1_rpc = BitprimRPC(rpcport_node1)
    node2_rpc = BitprimRPC(rpcport_node2)

    res, value = node1_rpc.get_info()
    if res:
        print("Node 1 get info:")
        print(value)
    else:
        print("Node 1 rpc call for get_info error")

    res, value = node2_rpc.get_info()
    if res:
        print("Node 2 get info:")
        print(value)
    else:
        print("Node 2 rpc call for get_info error")

    node1.stop()
    node2.stop()

    node1.clean_files()
    node2.clean_files()
