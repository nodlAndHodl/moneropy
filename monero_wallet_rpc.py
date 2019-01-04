import logging
import requests
import json
from requests.auth import HTTPDigestAuth
import os
import binascii


class MoneroWalletRpc:
    def __init__(self, rpc_url:str, user=None, pwd=None):
        self.rpc_url = rpc_url
        self.user = user
        self.password = pwd
        self.headers = {'content-type': 'application/json'}
        self.update = {"jsonrpc": "2.0", "id": "0"}
        self.rpc_input = None

    def post_to_monero_wallet_rpc(self, method: str, params=None):
        if params is not None:
            rpc_input = json.dumps({"jsonrpc": "2.0", "id": "0",
                                    "method": method, "params": params})
        else:
            rpc_input = json.dumps({"jsonrpc": "2.0", "id": "0",
                                    "method": method})

        logging.info(json.dumps(json.loads(rpc_input), indent=4))
        
        response = requests.post(
            self.rpc_url,
            data=rpc_input,
            headers=self.headers,
            auth=HTTPDigestAuth(self.user, self.password)
        )

        logging.info(json.dumps(response.json(), indent=4))
        
        return response.json()

    def refresh(self):
        return self.post_to_monero_wallet_rpc("refresh")

    def prepare_multisig(self):
        return self.post_to_monero_wallet_rpc("prepare_multisig")

    def exchange_multisig_keys(self, *, multisig_info):
        params = {"multisig_info": multisig_info}
        return self.post_to_monero_wallet_rpc("exchange_multisig_keys", params)
        

    def make_multisig(self, *, multisig_info, threshold: int, password: str = None):
        params = {
            "multisig_info": multisig_info,
            "threshold": threshold}

        if password:
            params["password"] = password
        return self.post_to_monero_wallet_rpc("make_multisig", params)


    def finalize_multisig(self, *, multisig_info, password: str = None):
        params = {
            "multisig_info": multisig_info}

        if password:
            params["password"] = password
            
        return self.post_to_monero_wallet_rpc("finalize_multisig", params)

    def is_multisig(self):
        return self.post_to_monero_wallet_rpc("is_multisig")

    def sign_multisig(self, tx_data_hex=None):
        params = {"tx_data_hex" : tx_data_hex}
        
        return self.post_to_monero_wallet_rpc("sign_multisig", params=params)

    def submit_multisig(self, tx_data_hex=None):
        params = {"tx_data_hex" : tx_data_hex}
        return self.post_to_monero_wallet_rpc("submit_multisig", params=params)

    def export_multisig_info(self):
        return self.post_to_monero_wallet_rpc("export_multisig_info")

    def import_multisig_info(self, info=None):
        params = {"info":  info}
        return self.post_to_monero_wallet_rpc("import_multisig_info", params=params)    

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

    def import_key_images(self, keys:dict):
        dict_key = {}
        list_keysig = []
        for key_image, sig in keys:
            dict_key.update({"key_image": key_image,"signature": sig})
            list_keysig.append(dict_key)
            dict_key.clear()
        params = {"signed_key_images": list_keysig}
        return self.post_to_monero_wallet_rpc("import_key_images", params)

    def rescan_spent(self):
        return self.post_to_monero_wallet_rpc("rescan_spent")

    def start_mining(self,thread_count:int, background_mining:bool, ignore_battery:bool):

        if background_mining is True:
            background_mining_str = "true"
        else:
            background_mining_str = "false"

        if ignore_battery is True:
            ignore_battery_str = "true"
        else:
            ignore_battery_str = "false"

        params = {"threads_count": thread_count, "do_background_mining": background_mining_str, "ignore_battery": ignore_battery_str}
        return self.post_to_monero_wallet_rpc("start_mining", params)


    def stop_mining(self):
        return self.post_to_monero_wallet_rpc("stop_mining")

    def stop_wallet(self):
        return self.post_to_monero_wallet_rpc("stop_wallet")

    def get_languages(self):
        return self.post_to_monero_wallet_rpc("get_languages")


    #You need to have set the argument "–wallet-dir" when
    def create_wallet(self, *, wallet_name:str, password: str, language:str = "English"):
        params = {"filename": wallet_name, "password": password, "language": language}
        return self.post_to_monero_wallet_rpc("create_wallet", params)

    #You need to have set the argument "–wallet-dir" when
    def open_wallet(self, *, wallet_name:str, password:str=""):
        params = {"filename": wallet_name, "password": password}
        return self.post_to_monero_wallet_rpc("open_wallet", params)

    def close_wallet(self):
        return self.post_to_monero_wallet_rpc("close_wallet")

    def delete_address_book(self, address_index: int):
        params = {"index": address_index}
        return self.post_to_monero_wallet_rpc("delete_address_book", params)

    def add_address_book(self, address: str, payment_id: str=None, description: str=None):
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
        params = {"data": data, "address": address, "signature": signature}
        return self.post_to_monero_wallet_rpc("verify", params=params)

    def make_uri_payment(self, address:str, amount:int,
                         payment_id:str, tx_description:str, recipient_name:str ):
        params = {"address": address, "amount": amount, "payment_id": payment_id,
                  "tx_description" : tx_description, "recipient_name": recipient_name}
        return self.post_to_monero_wallet_rpc("make_uri", params)


    def transfer(self, transactions, mixin=7, payment_id=None):
        # standard json header
        headers = self.headers
        recipients = []
        for address, amount in transactions.items():
            int_amount = int(self.get_amount(amount))
            assert amount == float(self.get_money(str(int_amount))), "Amount conversion failed"
            recipients.append({"address": address, "amount": int_amount})

        params = {"destinations": recipients,
                  "mixin": mixin}

        if payment_id:
            params["payment_id"] = payment_id

        return self.post_to_monero_wallet_rpc("transfer", params)

    
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
