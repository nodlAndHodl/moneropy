import requests
import json
from requests.auth import HTTPDigestAuth
import os
import binascii


class MoneroWalletRpc:
    def __init__(self, rpc_url=str, user=None, pwd=None):
        self.rpc_url = rpc_url
        self.user = user
        self.password = pwd
        self.headers = {'content-type': 'application/json'}
        self.update = {"jsonrpc": "2.0", "id": "0"}
        self.rpc_input = None

    def post_to_monero_wallet_rpc(self, method: str, params=None):
        # define standard json header
        if params is not None:
            rpc_input = json.dumps({"jsonrpc": "2.0", "id": "0",
                                    "method": method, "params": params})
        else:
            rpc_input = json.dumps({"jsonrpc": "2.0", "id": "0",
                                    "method": method})
        response = requests.post(
            self.rpc_url,
            data=rpc_input,
            headers=self.headers,
            auth=HTTPDigestAuth(self.user, self.password)
        )
        return json.dumps(response.json(), indent=5)

    def get_balance(self):
        return self.post_to_monero_wallet_rpc("getbalance")

    def get_address(self):
        return self.post_to_monero_wallet_rpc("getaddress")

    def get_height(self):
        return self.post_to_monero_wallet_rpc("getheight")

    def sweep_dust(self):
        return self.post_to_monero_wallet_rpc("sweep_dust")

    def get_payments(self, payment_id):
        params = {"wallet_address": payment_id}
        return self.post_to_monero_wallet_rpc("payment_id", params)

    def export_key_images(self):
        return self.post_to_monero_wallet_rpc("export_key_images")

    def import_key_images(self, keys):
        dict_key = {}
        list_keysig = []
        for key_image, sig in keys:
            dict_key.update({"key_image": key_image,"signature": sig})
            list_keysig.append(dict_key)
            dict_key.clear()
        params = {"signed_key_images":list_keysig}
        return self.post_to_monero_wallet_rpc("import_key_images", params)
        


        params = {"signed_key_images": [{}]}
    def rescan_spent(self):
        return self.post_to_monero_wallet_rpc("rescan_spent")


    def start_mining(self,thread_count:int, background_mining:bool, ignore_battery:bool):
        #TODO replace params
        data = '{"jsonrpc":"2.0","id":"0",' \
               '"method":"start_mining",' \
               '"params":{"threads_count":1,' \
               '"do_background_mining":true,' \
               '"ignore_battery":true}}'
        response = requests.post('http://localhost:18082/json_rpc', headers=self.headers, data=data)
        return json.dumps(response.json(), indent=5)

    def stop_mining(self):
        return self.post_to_monero_wallet_rpc("stop_mining")

    def stop_wallet(self):
        return self.post_to_monero_wallet_rpc("stop_wallet")

    def get_languages(self):
        return self.post_to_monero_wallet_rpc("get_languages")


    #TODO You need to have set the argument "–wallet-dir" when
    def create_wallet(self, wallet_name=str, password=str):
        params = {"filename": wallet_name, "password": password}
        return self.post_to_monero_wallet_rpc("create_wallet", params)


    # TODO You need to have set the argument "–wallet-dir" when
    def open_wallet(self, wallet_name=str, password=str):
        params = {"filename": wallet_name, "password": password}
        return self.post_to_monero_wallet_rpc("open_wallet", params)

    def delete_address_book(self, address_index: int):
        params = {"index": address_index}
        return self.post_to_monero_wallet_rpc("delete_address_book", params)

    def add_address_book(self, address: str, payment_id: str=None, description:str=None):
        params = {"address": address}
        if payment_id is not None:
            params.update({"payment_id":payment_id})
        if description is not None:
            params.update({"description":description})
        return self.post_to_monero_wallet_rpc("add_address_book", params)

    def sign(self, data: str):
        params = {"data": data}
        return self.post_to_monero_wallet_rpc("sign", params)

    def verify(self, data: str, address: str, signature:str):
        params = {"data": data,"address":address,"signature":signature}
        return self.post_to_monero_wallet_rpc("verify", params=params)

    def transfer(self, transactions, mixin=4,):
        url = self.rpc_url
        # standard json header
        headers = self.headers
        recipients = []
        for address, amount in transactions.items():
            int_amount = int(self.get_amount(amount))
            assert amount == float(self.get_money(str(int_amount))), "Amount conversion failed"
            recipients.append({"address": address, "amount": int_amount})
        print(recipients)
        # get some random payment_id
        payment_id = self.get_payment_id()
        # simplewallet' procedure/method to call
        rpc_input = {
            "method": "transfer",
            "params": {"destinations": recipients,
                       "mixin": mixin,
                       "payment_id": payment_id}
        }
        # add standard rpc values
        rpc_input.update({"jsonrpc": "2.0", "id": "0"})

        # execute the rpc request
        response = requests.post(
            url,
            data=json.dumps(rpc_input),
            headers=headers,
            auth=HTTPDigestAuth(self.user, self.password))
        # print the payment_id
        print("#payment_id: ", payment_id)
        # pretty print json output
        print(json.dumps(response.json(), indent=4))


    def get_amount(self, amount):
        """encode amount (float number) to the cryptonote format. Hope its correct.
        Based on C++ code:
        https://github.com/monero-project/bitmonero/blob/master/src/cryptonote_core/cryptonote_format_utils.cpp#L211
        """
        cryptonote_display_decimal_point = 12
        str_amount = str(amount)
        fraction_size = 0
        if '.' in str_amount:
            point_index = str_amount.index('.')
            fraction_size = len(str_amount) - point_index - 1
            while fraction_size < cryptonote_display_decimal_point and '0' == str_amount[-1]:
                print(44)
                str_amount = str_amount[:-1]
                fraction_size = fraction_size - 1
            if cryptonote_display_decimal_point < fraction_size:
                return False
            str_amount = str_amount[:point_index] + str_amount[point_index+1:]
        if not str_amount:
            return False
        if fraction_size < cryptonote_display_decimal_point:
            str_amount = str_amount + '0'*(cryptonote_display_decimal_point - fraction_size)
        return str_amount


    def get_money(self, amount):
        """decode cryptonote amount format to user friendly format. Hope its correct.
        Based on C++ code:
        https://github.com/monero-project/bitmonero/blob/master/src/cryptonote_core/cryptonote_format_utils.cpp#L751
        """
        cryptonote_display_decimal_point = 12
        s = amount
        if len(s) < cryptonote_display_decimal_point + 1:
            # add some trailing zeros, if needed, to have constant width
            s = '0' * (cryptonote_display_decimal_point + 1 - len(s)) + s
        idx = len(s) - cryptonote_display_decimal_point
        s = s[0:idx] + "." + s[idx:]
        return s


    def get_payment_id(self):
        random_32_bytes = os.urandom(32)
        payment_id = "".join(map(chr, binascii.hexlify(random_32_bytes)))
        return payment_id


    def make_uri_payment(self, address:str, amount:int,
                         payment_id:str, tx_description:str, recipient_name:str ):
        data = '{"jsonrpc":"2.0","id":"0","method":"make_uri",' \
               '"params":{"address":"44AFFq5kSiGBoZ4NMDwYtN18obc8AemS33DBLWs3H7otXft3XjrpDtQGv7SqSsaBYBb98uNbr2VBBEt7f2wfn3RVGQBEP3A",' \
               '"amount":10,"payment_id":"0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",' \
               '"tx_description":"Testing out the make_uri function.",' \
               '"recipient_name":"Monero Project donation address"}}'
        response = requests.post(
            self.rpc_url,
            data=data,
            headers=self.headers,
            auth=HTTPDigestAuth(self.user, self.password))
        return json.dumps(response.json(), indent=5)
