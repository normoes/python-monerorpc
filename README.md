# python-monerorpc
**python-monerorpc** is an improved version of python-jsonrpc for Monero (`monerod rpc`, `monero-wallet-rpc`).

**python-monerorpc** was originally forked from [**python-bitcoinrpc**](https://github.com/jgarzik/python-bitcoinrpc).

It includes the following generic improvements:

- HTTP connections persist for the life of the `AuthServiceProxy` object using `requests.Session`
- sends protocol 'jsonrpc', per JSON-RPC 2.0
- sends proper, incrementing 'id'
- uses standard Python json lib
- can optionally log all RPC calls and results
- JSON-2.0 batch support (mimicking batch)
  + JSON-2.0 batch doesn't seem to work with monero.
  + The batch functionality is mimicked and just requests the given methods one after another.
  + The result is a list of dictionaries.

It also includes some more specific details:

- sends Digest HTTP authentication headers
- parses all JSON numbers that look like floats as Decimal,
  and serializes Decimal values to JSON-RPC connections.

What does it do?
---
**python-monerorpc** communicates with monero over RPC.

That includes:
* `monerod rpc` as well as
* `monero-wallet-rpc`.

**python-monerorpc** takes over the actual HTTP request containing all the necessary headers.

## Compared to similar projects:
* [**monero-python**](https://github.com/emesik/monero-python)
  - **monero-python**
  - The module implements a json RPC backend (`monerod rpc`, `monero-wallet-rpc`).
  - It implements implementations around this backend (accounts, wallets, transactions, etc. )
  - It offers helpful utilities like a monero wallet address validator.
* A practical difference:
  - Should a RPC method change or a new one should be added, **monero-python** would have to adapt its backend and the implementations around it, while with **python-monerorpc** you just have to modify the property or use a new method like:

  ```python
      rpc_connection.getbalance() -> rpc_connection.get_balance()
      rpc_connection.new_method()
  ```


## Installation:
- change the first line of `setup.py` to point to the directory of your installation of python 2.*
- run `python setup.py install --user`

**Note**: This will only install `monerorpc`. If you also want to install `jsonrpc` to preserve
backwards compatibility, you have to replace `monerorpc` with `jsonrpc` in `setup.py` and run it again.

## Examples:
Example usage `monerod` (get info):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18081/json_rpc'.format(rpc_user, rpc_password))

    info = rpc_connection.get_info()
    print(info)

    # rpc_user and rpc_password can also be left out (testing, develop, not recommended)
    rpc_connection = AuthServiceProxy('http://127.0.0.1:18081/json_rpc')
```

Example usage `monerod` (get network type):

```python
  from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
  rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18081/json_rpc'.format(rpc_user, rpc_password))

  result = None
  network_type = None
  try:
      result = rpc_connection.get_info()
  except (requests.HTTPError,
          requests.ConnectionError,
          JSONRPCException) as e:
      logger.error('RPC Error on getting address' + str(e))
      logger.exception(e)
  # Check network type
  network_type = result.get('nettype')
  if not network_type:
      raise ValueError('Error with: {0}'.format(result))
  print(network_type)
```

Example usage `monero-wallet-rpc` (get balance):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18083/json_rpc'.format(rpc_user, rpc_password))

    balance = rpc_connection.get_balance()
    print(balance)
```

Example usage `monero-wallet-rpc` (make transfer):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18083/json_rpc'.format(rpc_user, rpc_password))

    destinations = {"destinations": [{"address": "some_address", "amount": 1}], "mixin": 10}
    result = rpc_connection.transfer(destinations)
    print(result)
```

Example usage `monero-wallet-rpc` (batch):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
    import pprint

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18083/json_rpc'.format(rpc_user, rpc_password))

    # some example batch
    params={"account_index":0,"address_indices":[0,1]}
    result = rpc.batch_([ ["get_balance"], ["get_balance", params] ])
    pprint.pprint(result)

    # make transfer and get balance in a batch
    destinations = {"destinations": [{"address": "some_address", "amount": 1}], "mixin": 10}
    result = rpc.batch_([ ["transfer", destinations], ["get_balance"] ])
    pprint.pprint(result)
```

## Logging:
Logging all RPC calls to stderr:

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
    import logging

    logging.basicConfig()
    logging.getLogger("MoneroRPC").setLevel(logging.DEBUG)

    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18081/json_rpc'.format(rpc_user, rpc_password))

    print(rpc_connection.get_info())
```

Produces output on stderr like:

```bash
    DEBUG:MoneroRPC:-1-> get_info []
    DEBUG:MoneroRPC:<-1- {u'result': {u'incoming_connections_count': 0, ...etc }
```
