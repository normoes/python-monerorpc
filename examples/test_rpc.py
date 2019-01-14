from monerorpc.authproxy import AuthServiceProxy, JSONRPCException
import logging

logging.basicConfig()
logging.getLogger("MoneroRPC").setLevel(logging.DEBUG)
log = logging.getLogger("wallet-rpc-lib")

rpc = AuthServiceProxy("http://test:test@127.0.0.1:38083/json_rpc")
# rpc = AuthServiceProxy('http://127.0.0.1:38083/json_rpc')
try:
    rpc.get_balance()
    params = {"account_index": 0, "address_indices": [0, 1]}
    rpc.get_balance(params)
    destinations = {
        "destinations": [
            {
                "address": "59McWTPGc745SRWrSMoh8oTjoXoQq6sPUgKZ66dQWXuKFQ2q19h9gvhJNZcFTizcnT12r63NFgHiGd6gBCjabzmzHAMoyD6",
                "amount": 1,
            }
        ],
        "mixin": 10,
    }
    rpc.transfer(destinations)
except (JSONRPCException) as e:
    log.error(e)
