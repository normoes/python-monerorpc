from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
logging.basicConfig()
logging.getLogger("MoneroRPC").setLevel(logging.DEBUG)
log = logging.getLogger("wallet-rpc-lib")

rpc = AuthServiceProxy('http://test:test@127.0.0.1:18081/json_rpc')
#rpc = AuthServiceProxy('http://127.0.0.1:18081/json_rpc')
try:
    rpc.get_block_count()
    params = [2]
    hash = rpc.on_get_block_hash(params)
    print(hash)
except (JSONRPCException) as e:
    log.error(e)
