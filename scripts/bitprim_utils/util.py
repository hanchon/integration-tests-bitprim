from binascii import hexlify, unhexlify
from base64 import b64encode
import hashlib
import time
import configparser


# Parser configuration file
def parse_cfg(cfg):
    config = configparser.ConfigParser(strict=False)
    config.read(cfg)
    rpc = config.get('node', 'rpc_port', fallback="18333")
    archive_directory = config.get('log', 'archive_directory', fallback="log-bch-testnet/archive")
    debug_file = config.get('log', 'debug_file', fallback="log-bch-testnet/debug.log")
    error_file = config.get('log', 'error_file', fallback="log-bch-testnet/error.log")
    hosts_file = config.get('network', 'hosts_file', fallback="hosts-bch-testnet.cache")
    directory = config.get('database', 'directory', fallback="database-bch-testnet")
    return rpc, archive_directory, debug_file, error_file, hosts_file, directory


# Encode / Decode utils
def bytes_to_hex_str(byte_str):
    return hexlify(byte_str).decode('ascii')


def hash256(byte_str):
    sha256 = hashlib.sha256()
    sha256.update(byte_str)
    sha256d = hashlib.sha256()
    sha256d.update(sha256.digest())
    return sha256d.digest()[::-1]


def hex_str_to_bytes(hex_str):
    return unhexlify(hex_str.encode('ascii'))


def str_to_b64str(string):
    return b64encode(string.encode('utf-8')).decode('ascii')


# Asserts
def assert_equal(thing1, thing2, *args):
    if thing1 != thing2 or any(thing1 != arg for arg in args):
        raise AssertionError("not(%s)" % " == ".join(str(arg)
                                                     for arg in (thing1, thing2) + args))


def assert_greater_than(thing1, thing2):
    if thing1 <= thing2:
        raise AssertionError("%s <= %s" % (str(thing1), str(thing2)))


def assert_greater_than_or_equal(thing1, thing2):
    if thing1 < thing2:
        raise AssertionError("%s < %s" % (str(thing1), str(thing2)))


# Node syncs
def sync_chain(nodes, *, wait=1, timeout=60):
    """
    Wait until everybody has the same best block
    """
    while timeout > 0:
        best_hash = [x.rpc.generate_best_block_hash() for x in nodes]
        if best_hash == [best_hash[0]] * len(best_hash):
            return
        time.sleep(wait)
        timeout -= wait
    raise AssertionError("Chain sync failed: Best block hashes don't match")