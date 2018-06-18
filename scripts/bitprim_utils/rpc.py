import subprocess
import requests


class BitprimRPC:

    def __init__(self, rpcport):
        self.rpcport = rpcport
        self.address = "http://127.0.0.1:" + str(self.rpcport)

    def send_curl(self, payload):
        headers = {'content-type': 'text/plain;'}
        return requests.post(self.address, data=payload, headers=headers)

    @staticmethod
    def validate_curl_response(response):
        if response.status_code == requests.codes.ok:
            return True, response.json()
        return False, ""

    def get_info(self):
        payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }'
        return self.validate_curl_response(self.send_curl(payload))

    def get_block_hash(self, height):
        payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [' + str(
            height) + '] }'
        return self.validate_curl_response(self.send_curl(payload))

    def get_block(self, hash_value):
        payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["' + str(
            hash_value) + '"] }'
        return self.validate_curl_response(self.send_curl(payload))
