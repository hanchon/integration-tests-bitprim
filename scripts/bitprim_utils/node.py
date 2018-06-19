import os
import subprocess
import time
from .rpc import BitprimRPC
from bitprim_utils.util import (
    parse_cfg,
)


class BitprimNode:

    def __init__(self, config_file, binary, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):

        self.config_file = config_file

        self.rpcport, self.archive_directory, self.debug_file, self.error_file, self.hosts_file, self.directory = parse_cfg(
            config_file)

        if binary is None:
            self.binary = os.getenv("BITPRIM", "../bn")
        else:
            self.binary = binary

        self.stdout = stdout
        self.stderr = stderr

        self.running = False
        self.process = None

        self.rpc = BitprimRPC(self.rpcport)

    def start(self, stdout=None, stderr=None):
        """Start the node."""
        if stdout is None:
            stdout = self.stdout
        if stderr is None:
            stderr = self.stderr
        # Initiate databases
        print("Running init node: " + str(self.config_file))
        self.process = subprocess.Popen([self.binary, "-i", "-c", self.config_file], stdout=stdout, stderr=stderr)
        self.wait_until_process_end()
        print("Init ended  node: " + str(self.config_file))

        # Run the node
        print("Running the node: " + str(self.config_file))
        self.process = subprocess.Popen([self.binary, "-c", self.config_file], stdout=stdout, stderr=stderr)

        # TODO: validate that the is node is runing and ready to response rpc requests
        # Send getinfos until the node start to answer the requests
        self.running = True

    def stop_call(self):
        self.process.terminate()

    def stop(self):
        """Stop the node."""
        if not self.running:
            return
        print("Stopping the node: " + str(self.config_file))
        self.stop_call()
        self.wait_until_process_end()
        print("Node stopped successfully: " + str(self.config_file))

    def wait_until_process_end(self):
        while self.process.poll() is None:
            time.sleep(1)
            print('.', end='', flush=True)
        print("")

    def clean_files(self):
        os.system('rm -rf ' + self.archive_directory)
        os.system('rm -rf ' + self.directory)
        os.system('rm -rf ' + self.hosts_file)