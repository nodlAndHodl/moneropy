import requests
import json


class MoneroDaemonRpc:

    def __init__(self, rpc_url=str):
        self.rpc_url = rpc_url
        self.headers = {'Content-Type': 'application/json'}

    def post_to_monerod_rpc(self, method=str, *params):
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
            headers=self.headers
        )
        return json.dumps(response.json(), indent=5)

    def get_block_count(self):
        return self.post_to_monerod_rpc("getblockcount")

    def on_getblockhash(self, block=int):
        return self.post_to_monerod_rpc("on_getblockhash", block)

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

    def set_bans(self):
        #TODO add list to input parameters and create ban object
        #For some reason method not found but is in documentation
        '''{
             "error": {
                  "message": "Method not found",
                  "code": -32601
             },
             "id": "0",
             "jsonrpc": "2.0"
        }
        '''
        data = '{"jsonrpc":"2.0","id":"0","method":"set_bans","params":{"bans":[{"ip":838969536,"ban":true,"seconds":30}]}}'
        response = requests.post(self.rpc_url, headers=self.headers, data=data)
        print(response.headers)
        return json.dumps(response.json(), indent=5)

    def stop_daemon(self):
        url = self.rpc_url.replace('json_rpc', 'stop_daemon')
        response = requests.post(url, headers=self.headers)

    #get_transaction_pool
    def get_transaction_pool(self):
        #TODO this is causing some issues with json decoding
        response = requests.get('http://127.0.0.1:18081/get_transaction_pool', headers=self.headers)
        print(response.headers)
        return json.dumps(response.json())

