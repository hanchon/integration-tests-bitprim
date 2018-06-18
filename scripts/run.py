from bitprim_utils.node import BitprimNode
import time

if __name__ == "__main__":
    node1 = BitprimNode(1, 18333, "../config/bch/cfg", "./bn")
    node1.start()

    node2 = BitprimNode(2, 18335, "../config/bch/cfg", "./bn")
    node2.start()

    time.sleep(60)

    node1.stop()
    node2.stop()

    node1.clean_files()
    node2.clean_files()
