# python-monerorpc

**DISCLAIMER**: The repository that should be worked on is located at the [**monero-ecosystem**](https://github.com/monero-ecosystem/python-monerorpc).

**python-monerorpc** is an improved version of python-jsonrpc for Monero (`monerod rpc`, `monero-wallet-rpc`).

**python-monerorpc** was originally forked from [**python-bitcoinrpc**](https://github.com/jgarzik/python-bitcoinrpc).

It includes the following generic improvements:

- HTTP connections persist for the life of the `AuthServiceProxy` object using `requests.Session`
- sends protocol 'jsonrpc', per JSON-RPC 2.0
- sends proper, incrementing 'id'
- uses standard Python json lib
- can optionally log all RPC calls and results
- JSON-2.0 batch support (mimicking batch)
  - JSON-2.0 batch doesn't seem to work with monero.
  - The batch functionality is mimicked and just requests the given methods one after another.
  - The result is a list of dictionaries.

It also includes some more specific details:

- sends Digest HTTP authentication headers
- parses all JSON numbers that look like floats as Decimal,
  and serializes Decimal values to JSON-RPC connections.

## What does it do?

**python-monerorpc** communicates with monero over RPC.

That includes:

- `monerod rpc` as well as
- `monero-wallet-rpc`.

**python-monerorpc** takes over the actual HTTP request containing all the necessary headers.

## Compared to similar projects:

- [**monero-python**](https://github.com/monero-ecosystem/monero-python)
  - **monero-python**
  - The module implements a json RPC backend (`monerod rpc`, `monero-wallet-rpc`).
  - It implements implementations around this backend (accounts, wallets, transactions, etc. )
  - It offers helpful utilities like a monero wallet address validator.
- A practical difference:

  - Should a RPC method change or a new one should be added, **monero-python** would have to adapt its backend and the implementations around it, while with **python-monerorpc** you just have to modify the property or use a new method like:

  ```python
      rpc_connection.getbalance()  # -> rpc_connection.get_balance()
      rpc_connection.new_method()
  ```
## Errors

The `JSONRPCException` is thrown in the event of an error.

One exception to that rule is when receiving a `JSONDecodeError` when converting the response to JSON.
In this case a `ValueError` including the HTTP response is raised.

This error was not handled before and directly raised a `JSONDecodeError`. Since `JSONDecodeError` inherits from `ValueError` nothing really changes. You should handle `ValueError` in addition to just `JSONRPCException` when working with `python-monerorpc`.

**_TODO_**:
An improved error handling.
* Provide detailed information.
* Separate into several causes like connection error, conversion error, etc.

## Installation:

### From PyPI

To install `python-monerorpc` from PyPI using `pip` you just need to:

> \$ pip install python-monerorpc

### From Source

> \$ python setup.py install --user

**Note**: This will only install `monerorpc`. If you also want to install `jsonrpc` to preserve
backwards compatibility, you have to replace `monerorpc` with `jsonrpc` in `setup.py` and run it again.

## Examples:

Example usage `monerod` (get info):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy(service_url='http://{0}:{1}@127.0.0.1:18081/json_rpc'.format(rpc_user, rpc_password))

    info = rpc_connection.get_info()
    print(info)

    # rpc_user and rpc_password can also be left out (testing, develop, not recommended)
    rpc_connection = AuthServiceProxy(service_url='http://127.0.0.1:18081/json_rpc')
```

Example usage `monerod` (special characters in RPC password).

This is also the recommended way to use passwords containing special characters like `some_password#-+`.

When both ways are used (username/password in the URL and passed as arguments), the arguments' values will be predominant.

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # When leaving rpc_user and rpc_password in the URL,
    # you can still pass those values as separate paramaters.
    rpc_connection = AuthServiceProxy(service_url='http://127.0.0.1:18081/json_rpc', username=rpc_user, password=rpc_password)

    # Or use both ways.
    rpc_connection = AuthServiceProxy(service_url='http://{0}@127.0.0.1:18081/json_rpc'.format(rpc_user), password=rpc_password)
```

Example usage `monerod` (get network type):

```python
  from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
  rpc_connection = AuthServiceProxy(service_url='http://{0}:{1}@127.0.0.1:18081/json_rpc'.format(rpc_user, rpc_password))

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

Example usage `monerod` (on get block hash):

```python
  from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
  rpc_connection = AuthServiceProxy(service_url='http://{0}:{1}@127.0.0.1:18081/json_rpc'.format(rpc_user, rpc_password))

  params = [2]
  hash = rpc.on_get_block_hash(params)
  print(hash)
```

Example usage `monero-wallet-rpc` (get balance):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy(service_url='http://{0}:{1}@127.0.0.1:18083/json_rpc'.format(rpc_user, rpc_password))

    balance = rpc_connection.get_balance()
    print(balance)
```

Example usage `monero-wallet-rpc` (make transfer):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy(service_url='http://{0}:{1}@127.0.0.1:18083/json_rpc'.format(rpc_user, rpc_password))

    destinations = {"destinations": [{"address": "some_address", "amount": 1}], "mixin": 10}
    result = rpc_connection.transfer(destinations)
    print(result)
```

Example usage `monero-wallet-rpc` (batch):

```python
    from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
    import pprint

    # initialisation, rpc_user and rpc_password are set as flags in the cli command
    rpc_connection = AuthServiceProxy(service_url='http://{0}:{1}@127.0.0.1:18083/json_rpc'.format(rpc_user, rpc_password))

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

    rpc_connection = AuthServiceProxy(service_url='http://{0}:{1}@127.0.0.1:18081/json_rpc'.format(rpc_user, rpc_password))

    print(rpc_connection.get_info())
```

Produces output on stderr like:

```bash
    DEBUG:MoneroRPC:-1-> get_info []
    DEBUG:MoneroRPC:<-1- {u'result': {u'incoming_connections_count': 0, ...etc }
```

## Errors:

Possible errors and error codes:

- `no code`
  - Returns the `error` contained in the RPC response.
- `-341`
  - `could not establish a connection, original error: {}`
  - including the original exception message
- `-342`
  - `missing HTTP response from server`
- `-343`
  - `missing JSON-RPC result`
- `-344`
  - `received HTTP status code {}`
  - including HTTP status code other than `200`

## Testing:

Install the test requirements:

```bash
    python -m venv venv
    # virtualenv -q venv
    . venv/bin/activate
    pip install -r requirements.txt
```

Run unit tests using `pytest`:

```bash
    # virtualenv activated (see above)
    pytest tests.py
```

Run unit tests on all supported python versions:

```bash
    tox -q
```

Run unit tests on a subset of the supported python versions:

```bash
    tox -q -e py27,py34
```

**Note:** The chosen python versions have to be installed on your system.

## Authors

- **Norman Moeschter-Schenck** - _Initial work_ - [normoes](https://github.com/normoes)

See also the list of [contributors](https://github.com/monero-ecosystem/python-monerorpc/blob/master/contributors.md) who participated in this project.
