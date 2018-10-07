# python-monerorpc
**python-monerorpc** is an improved version of python-jsonrpc for Monero (`monerod rpc`, `monero-wallet-rpc`).

**python-monerorpc** was originally forked from [**python-bitcoinrpc**](https://github.com/jgarzik/python-bitcoinrpc).

It includes the following generic improvements:

- HTTP connections persist for the life of the `AuthServiceProxy` object using `requests.Session`
- sends protocol 'jsonrpc', per JSON-RPC 2.0
- sends proper, incrementing 'id'
- uses standard Python json lib
- can optionally log all RPC calls and results
- JSON-2.0 batch support

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

  ```
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

```
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18081'.format(rpc_user, rpc_password))
    info = rpc_connection.get_info()
    print(info)
    # rpc_user and rpc_password can also be left out (testing, develop, not recommended)
    rpc_connection = AuthServiceProxy('http://127.0.0.1:18081')
```

Example usage `monero-wallet-rpc` (get balance):

```
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18083'.format(rpc_user, rpc_password))
    balance = rpc_connection.get_balance()
    print(balance)
```

Example usage `monero-wallet-rpc` (make transfer):

```
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18083'.format(rpc_user, rpc_password))
    destinations = {"destinations": [{"address": "some_address", "amount": 1}], "mixin": 10}
    result = rpc_connection.transfer(destinations)
    print(result)
```

## Logging:
Logging all RPC calls to stderr:

```
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
    import logging
    logging.basicConfig()
    logging.getLogger("MoneroRPC").setLevel(logging.DEBUG)
    rpc_connection = AuthServiceProxy('http://{0}:{1}@127.0.0.1:18081'.format(rpc_user, rpc_password))
    print(rpc_connection.get_info())
```

Produces output on stderr like:

```
    DEBUG:MoneroRPC:-1-> get_info []
    DEBUG:MoneroRPC:<-1- {u'result': {u'incoming_connections_count': 0, ...etc }
```
