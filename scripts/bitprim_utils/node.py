import os
import logging
import subprocess
import time


class BitprimNode:

    def __init__(self, i, rpcport, config_file, binary, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
        self.index = i
        self.rpcport = rpcport

        self.config_file = config_file

        if binary is None:
            self.binary = os.getenv("BITPRIM", "./bn")
        else:
            self.binary = binary

        self.stdout = stdout
        self.stderr = stderr

        # self.cli = TestNodeCLI(os.getenv("BITCOINCLI", "bitcoin-cli"), self.datadir)

        self.running = False
        self.process = None

        self.log = logging.getLogger('Bitprim.node%d' % i)

    def start(self, stdout=None, stderr=None):
        """Start the node."""
        if stdout is None:
            stdout = self.stdout
        if stderr is None:
            stderr = self.stderr
        # Initiate databases
        print("Running init node " + str(self.index))
        self.process = subprocess.Popen([self.binary, "-i", "-c", self.config_file + str(self.index)], stdout=stdout,
                                        stderr=stderr)
        self.wait_until_process_end()
        print("Init ended  node " + str(self.index))

        # Run the node
        print("Running the node  " + str(self.index))
        self.process = subprocess.Popen([self.binary, "-c", self.config_file + str(self.index)], stdout=stdout,
                                        stderr=stderr)
        self.running = True
        # self.log.debug("bitcoind started, waiting for RPC to come up")

    def stop_call(self):
        self.process.terminate()

    def stop(self):
        """Stop the node."""
        if not self.running:
            return
        # self.log.debug("Stopping node")
        print("Stopping the node " + str(self.index))
        self.stop_call()
        self.wait_until_process_end()
        print("Node " + str(self.index) + " stopped successfully")

    def wait_until_process_end(self):
        while self.process.poll() is None:
            time.sleep(1)
            print('.', end='', flush=True)
        print("")

    def clean_files(self):
        os.system('rm -rf ./database-bch-testnet' + str(self.index))
        os.system('rm -rf ./log-bch-testnet' + str(self.index))
        os.system('rm -rf ./host-bch-testnet' + str(self.index) + '.cache')


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
