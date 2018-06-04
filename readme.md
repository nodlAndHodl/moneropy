# Monero RPC Daemon and Monero Wallet RPC
This project was designed with helping python developers who are interested in Monero and the Monero Blockchain. This is a basic implementation
of using the Monero RPC daemon for querying the blockchain and using the wallet RPC for sending and confirming txn's amongst other things.
I basically took the developer's guide from monero and created this simple library as a side project.
You can visit the site here: https://getmonero.org/resources/developer-guides
## Getting Started

Recommended for running both libraries is a download of the monero daemon cli and the wallet cli.
For instructions on getting started with monero go to https://getmonero.org/get-started/what-is-monero/ and for downloads of the monero client go to https://getmonero.org/downloads/ . 

I have found that there were many other tutorials on using python for doing what this library does, but they were not implemented in a way that made the code reusable. Hope this helps others
and that they contribute to the community of blockchain developers and enthusiasts. 

### Prerequisites

This library was developed on Python Version 3.5.2, and has not been tested on other versions of python, but should run on 3.2 and higher. Nothing fancy library wise was used.
json, and requests are both used which come by default with most python installs. Also you'll need to have a monero install if you want to run the wallet rpc. 

### Installing
I may turn this into a pipable library, but for now just download or clone. 

### Example of using code...
```python
#CLI args for testnet look like monerod --testnet

#This is how you'd use the MoneroDaemonRpc
from monerojdaemon import MoneroDaemonRpc

rpc = MoneroDaemonRpc("http://127.0.0.1:18081/json_rpc", user='username', password='password')
rpc.get_block(89138)


#CLI args for testnet look like:
#monero-wallet-rpc --wallet-file test-net --password test --daemon-address  127.0.0.1:28081 --rpc-bind-port 28082 --rpc-login username:password
#This is how you could use the MoneroWalletRpc
from monero_wallet_rpc import MoneroWalletRpc

wallet = MoneroWalletRpc("http://127.0.0.1:28082/json_rpc", 'username', 'password')

transaction_dict = {
     "9uUr8urCW73Hf1S2PxDkmKBk8wRujbSNuVgusyUDGv5seSjbKwDATafCXAmbWd8cWHghhzF2J4hpGLXEkUkxHCT35A4VaU3": 0.0010001,
     "9w3GEk4HpjZFGMp8hq56fuaZTC4RVzdpbMVD5mw2kKK9afoQJRNXfYaaEsZpo5yY4S3ruNKqF8nF7dnpPsFysFRrFnXbWu8": 0.00227}
#
print(wallet.transfer(transaction_dict, 10))
print(wallet.get_balance())

```

### Support if you are able to or find this useful in your projects.

XMR address: 89FheVhwYVzWCVjgfTYKrFSYs9V7bASszTHn3JyVsdgsXr9cVgHQGhK9Haynypqt6vAXFzRKZo4yLffLJeed42ChCpMrovt  
ZEC address: t1STUKUuzpqFh55JiERXJtFLHPdCk43PWmP  
ETH address: 0xb2d8bef2b364e3f421db24c145fcfc3705eb78c1  
LTC address: LepgPD7PN1deUQDRPxrpYL8XUMVsrKPhiz  
BCH address: 12q7Yh1L4xP5wdS9WYd12NCuz9boQErrje  
BTC address: 1FUPCpA6ttSPLJreJk8f8sjbP5Q122zmbg  



