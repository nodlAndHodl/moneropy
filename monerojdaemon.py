import requests
import json
from requests.auth import HTTPDigestAuth

class MoneroDaemonRpc:

    def __init__(self, rpc_url: str, *user: str):
        self.rpc_url = rpc_url
        self.headers = {'Content-Type': 'application/json'}
        self.user = user[0]
        self.password = [1]

    def post_to_monerod_rpc(self, method:str, *params):
        # define standard json header
        if params is not None:
            rpc_input = {"method": method, "params": params}
        else:
            rpc_input = {"method": method}
        # add standard rpc values
        rpc_input.update({"jsonrpc": "2.0", "id": "0"})
        # execute the rpc request
        response = requests.post(
            self.rpc_url,
            data=json.dumps(rpc_input),
            headers=self.headers,
            auth=HTTPDigestAuth(self.user, self.password)
        )
        return json.dumps(response.json(), indent=5)

    def get_block_count(self):
        return self.post_to_monerod_rpc("getblockcount")

    def get_block(self, height=int):
        data = '{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":'+str(height)+'}}'
        response = requests.post(self.rpc_url, headers=self.headers, data=data)
        return json.dumps(response.json())

    def on_getblockhash(self, block=int):
        return self.post_to_monerod_rpc("on_getblockhash", block)

    def get_block_template(self, address=str, reserve_size=int):
        data = '{"jsonrpc":"2.0","id":"0","method":"getblocktemplate","params":{"wallet_address":"'+address+'","reserve_size":'+str(reserve_size)+'}'
        response = requests.post('http://127.0.0.1:18081/json_rpc', headers=self.headers, data=data)
        return json.dumps(response.json())

    def get_last_block_header(self):
        return self.post_to_monerod_rpc("getlastblockheader")

    def get_block_header_by_height(self, block_num=int):
        params = {"params": {"height": block_num}}
        return self.post_to_monerod_rpc("getblockheaderbyheight", params)

    def get_block_header_by_hash(self, hash=str):
        #TODO clean this up and find a better way to implement with other method of rpc_post method
        data = '{"jsonrpc":"2.0","id":"0","method":"getblockheaderbyhash","params":{"hash":"'+hash+'"}}'
        response = requests.post(self.rpc_url, headers=self.headers, data=data)
        return json.dumps(response.json(), indent=5)

    def get_connections(self):
        return self.post_to_monerod_rpc("get_connections")

    def get_info(self):
        return self.post_to_monerod_rpc("get_info")

    def get_hard_fork_info(self):
        return self.post_to_monerod_rpc("hard_fork_info")

    def get_fee_estimate(self):
        return self.post_to_monerod_rpc("get_fee_estimate")

    def submit_block(self, block_blob=str):
        data = r'{"jsonrpc": "2.0","id": "0", "method": "submitblock","params": '+ block_blob +'}'
        response = requests.post(self.rpc_url, headers=self.headers, data=data)
        return json.dumps(response.json())

    def set_bans(self):
        #TODO add list to input parameters and create ban object
        data = r'{"jsonrpc":"2.0","id":"0","method":"set_bans","params":{"bans":[{"ip":838969536,"ban":true,"seconds":30}]}}'
        response = requests.post(self.rpc_url, headers=self.headers, data=data)
        print(response.headers)
        return json.dumps(response.json(), indent=5)
        url = self.rpc_url.replace('json_rpc', 'stop_daemon')
        response = requests.post(url, headers=self.headers)

    def get_bans(self):
        return self.post_to_monerod_rpc("get_bans")

    #get_transaction_pool
    def get_transaction_pool(self):
        response = requests.get(self.rpc_url, headers=self.headers)
        print(response.headers)
        #This returns a text response(can parse into json with some additional work)
        return response.text

    def get_transactions(self, tx_hash=str):
        data = r'{"txs_hashes":["'+tx_hash+'"]}'
        #TODO replace rpc_url below
        url = self.rpc_url.replace('json_rpc', 'gettransactions')
        response = requests.post(url, headers=self.headers, data=data)
        return response.text

    def is_key_image_spent(self, key_images=list):
        data = '{"key_images":'+str(key_images)+' }'
        url = self.rpc_url.replace('json_rpc', 'is_key_image_spent')
        response = requests.post(url, headers=self.headers, data=data)
        return response.text

    def send_draw_transaction(self, tx_hash=str, do_not_relay=bool):
        data = ''
        if do_not_relay is True:
            data = '{"tx_as_hex":' + tx_hash + ', "do_not_relay":true}'
        else:
            data = '{"tx_as_hex":' + tx_hash + ', "do_not_relay":false}'
        url = self.rpc_url.replace('json_rpc', 'sendrawtransaction')
        response = requests.post(url, headers=self.headers, data=data)
        return response.text
