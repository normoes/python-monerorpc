from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
logging.basicConfig()
logging.getLogger("MoneroRPC").setLevel(logging.DEBUG)
log = logging.getLogger("wallet-rpc-lib")

rpc = AuthServiceProxy('http://test:test@127.0.0.1:38083/json_rpc')
#rpc = AuthServiceProxy('http://127.0.0.1:38083/json_rpc')
try:
  rpc.get_balance()
except (JSONRPCException) as e:
  log.error(e)
