# Integration tests bitprim
WIP use python to generate integration tests for a bitprim node.

# Requirements
* Python 3.X
  * `pip install requests`
  * `pip install configparser`
* Bitprim-exe with rpc.
```
cd integration-tests-bitprim
cd scripts
./download_bitprim.sh
```

# Run
```
git clone https://github.com/hanchon/integration-tests-bitprim
cd integration-tests-bitprim
cd scripts
python3 run.py
```
Make sure the `bn` is located on the `integration-tests-bitprim/scripts` folder