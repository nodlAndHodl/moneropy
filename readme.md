# Monero RPC Daemon and Monero Wallet RPC
This project was designed with helping python developers who are interested in Monero and the Monero Blockchain. This is a basic implementation
of using the Monero RPC daemon for querying the blockchain and using the wallet RPC for sending and confirming txn's amongst other things. 

## Getting Started

Recommended for running both libraries is a download of the monero daemon and the wallet cli. 
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
from monerojdaemon import MoneroDaemonRpc

rpc = MoneroDaemonRpc("http://127.0.0.1:18081/json_rpc", user='username', password='password')
rpc.get_block(89138)
```

