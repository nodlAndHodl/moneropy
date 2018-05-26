import requests
import json
from requests.auth import HTTPDigestAuth


class MoneroDaemonRpc:
    def __init__(self, rpc_url: str, user: str=None, password: str=None):
        self.rpc_url = rpc_url
        self.headers = {'Content-Type': 'application/json'}
        self.user = user
        self.password = password

    def post_to_monerod_rpc(self, method:str, *params: dict):
        # define standard json header
        if len(params) > 0 and params is not None:
            rpc_input = json.dumps({"jsonrpc": "2.0", "id": "0","method": method, "params": params[0]})
        else:
            rpc_input = json.dumps({"jsonrpc": "2.0", "id": "0","method": method})
        print(rpc_input)
        response = requests.post(
            self.rpc_url,
            data=rpc_input,
            headers=self.headers,
            auth=HTTPDigestAuth(self.user, self.password)
        )
        return json.dumps(response.json(), indent=5)

    def get_block_count(self):
        return self.post_to_monerod_rpc("getblockcount")

    def get_block(self, block):
        if type(block) is str:
            params = {"height": str(block)}
        if type(block) is int:
            params = {"height": block}
        return self.post_to_monerod_rpc("getblock", params)

    def on_getblockhash(self, block: int):
        return self.post_to_monerod_rpc("on_getblockhash", block)

    def get_block_template(self, address: str, reserve_size: int):

        params = {"wallet_address": address, "reserve_size": reserve_size}
        return self.post_to_monerod_rpc("getblocktemplate", params)

    def get_last_block_header(self):
        return self.post_to_monerod_rpc("getlastblockheader")

    def get_block_header_by_height(self, block_num: int):
        params = {"height": block_num}
        return self.post_to_monerod_rpc("getblockheaderbyheight", params)

    def get_block_header_by_hash(self, hash: str):
        params = {"hash": hash}
        return self.post_to_monerod_rpc("getblockheaderbyhash", params)

    def get_connections(self):
        return self.post_to_monerod_rpc("get_connections")

    def get_info(self):
        return self.post_to_monerod_rpc("get_info")

    def get_hard_fork_info(self):
        return self.post_to_monerod_rpc("hard_fork_info")

    def get_fee_estimate(self):
        return self.post_to_monerod_rpc("get_fee_estimate")

    def submit_block(self, block_blob: str):
        data = r'{"jsonrpc": "2.0","id": "0", "method": "submitblock","params": ' + block_blob + '}'
        response = requests.post(self.rpc_url, headers=self.headers, data=data)
        return json.dumps(response.json())

#TODO look into this more
    def set_bans(self, list_ips, time):
        #params = {"bans":[{"ip":838969536,"ban":true,"seconds":30}]}}
        #TODO add list to input parameters and create ban object/class
        data = r'{"jsonrpc":"2.0","id":"0","method":"set_bans","params":{"bans":[{"ip":838969536,"ban":true,"seconds":30}]}}'
        response = requests.post(self.rpc_url, headers=self.headers, data=data)
        print(response.headers)
        return json.dumps(response.json(), indent=5)

    def get_bans(self):
        return self.post_to_monerod_rpc("get_bans")

    def stop_daemon(self):
        url = self.rpc_url.replace('json_rpc', 'stop_daemon')
        response = requests.post(url, headers=self.headers)
        return json.dumps(response.json(), indent=5)

    #get_transaction_pool
    def get_transaction_pool(self):
        response = requests.get(self.rpc_url, headers=self.headers)
        print(response.headers)
        #This returns a text response(can parse into json with some additional work)
        return response.text

    def get_transactions(self, tx_hash=str):
        data = r'{"txs_hashes":["'+tx_hash+'"]}'
        url = self.rpc_url.replace('json_rpc', 'gettransactions')
        response = requests.post(url, headers=self.headers, data=data)
        return response.text

    def is_key_image_spent(self, key_images: list):
        keys = ""
        for key in key_images[:-1]:
            keys += '"' + key + '",'
        else:
            keys += '"' + key + '"'
        data = '{"key_images":['+keys+']}'
        url = self.rpc_url.replace('json_rpc', 'is_key_image_spent')
        response = requests.post(url, headers=self.headers, data=data)
        return response.text

    def send_draw_transaction(self, tx_hash=str, do_not_relay=bool):
        data = ''
        if do_not_relay is True:
            data = '{"tx_as_hex":'+tx_hash+', "do_not_relay":true}'
        else:
            data = '{"tx_as_hex":'+tx_hash+', "do_not_relay":false}'
        url = self.rpc_url.replace('json_rpc', 'sendrawtransaction')
        response = requests.post(url, headers=self.headers, data=data)
        return response.text


