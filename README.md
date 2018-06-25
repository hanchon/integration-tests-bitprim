# Integration tests bitprim
WIP use python to generate integration tests for a bitprim node.

# Requirements
* Python 3.X
  * `pip install requests`
  * `pip install configparser`

# Run
Clone the repository, download the `bn` binary and run the tests.
```
git clone https://github.com/hanchon/integration-tests-bitprim
cd integration-tests-bitprim
cd scripts
./download_bitprim.sh
python3 runner.py
```

# Results
The runner will print the stdout and stderr of the tests that failed.
After the error reports it'll show a table with an execution's summary.

```
/home/hanchon/devel/integration-tests-bitprim/venv/bin/python /home/hanchon/devel/integration-tests-bitprim/scripts/runner.py
................................................................
01_run_error.py failed, Duration: 32 s

stdout:
Running init node: ../config/bch/cfg1
Init ended  node: ../config/bch/cfg1
Running the node: ../config/bch/cfg1
Running init node: ../config/bch/cfg2
Init ended  node: ../config/bch/cfg2
Running the node: ../config/bch/cfg2
Node 1 get info:
{'error': None, 'id': 'curltest', 'result': {'blocks': 0, 'connections': 1, 'difficulty': 1, 'errors': '', 'protocolversion': 70013, 'proxy': '', 'relayfee': 0.0, 'testnet': True, 'timeoffset': 0, 'version': 120000}}
Node 2 get info:
{'error': None, 'id': 'curltest', 'result': {'blocks': 0, 'connections': 1, 'difficulty': 1, 'errors': '', 'protocolversion': 70013, 'proxy': '', 'relayfee': 0.0, 'testnet': True, 'timeoffset': 0, 'version': 120000}}
Node 1 best hash:
000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943
Node 2 best hash:
000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943


stderr:
Traceback (most recent call last):
  File "./01_run_error.py", line 44, in <module>
    assert_equal(1, 2)
  File "/home/hanchon/devel/integration-tests-bitprim/scripts/bitprim_utils/util.py", line 46, in assert_equal
    for arg in (thing1, thing2) + args))
AssertionError: not(1 == 2)


.....................................................................................................................................................................................................................
TEST            | STATUS    | DURATION

01_run_error.py | ✖ Failed  | 32 s
run.py          | ✓ Passed  | 156 s

ALL             | ✖ Failed  | 188 s (accumulated)
Runtime: 190 s
```