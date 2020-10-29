# import subprocess
# import json
# import os

# command = './derive -g --mnemonic="more silent beauty club calm again taste staff check poverty sport usual" --cols=path,address,privkey,pubkey --format=json'

# p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
# output, err = p.communicate()
# p_status = p.wait()

# keys = json.loads(output)
# print(keys)

# from constants import *

# mnemonic = os.getenv('MNEMONIC', 'barrel gasp approve wire torch erode climb green undo adjust weasel black people pony sea')


import subprocess
import json
import os
from constants import *
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

load_dotenv()

ETH = 'eth'
BTC = 'btc'
BTCTEST = 'btc-test'


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
mnemonic = os.getenv('MNEMONIC')


def derive_wallets (mnemonic, coin, numderive):

    command = './hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="'+str(mnemonic)+'" --numderive='+str(numderive)+' --coin='+str(coin)+' --format=jsonpretty' 
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return json.loads(output)

