import subprocess
import json
import os
from constants import *
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

load_dotenv()

# constants not able to import so I have listed them here
ETH = 'eth'
BTC = 'btc'
BTCTEST = 'btc-test'


# connect to local ETH/ geth
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
mnemonic = os.getenv('MNEMONIC')


p = subprocess.Popen(mnemonic, shell=True, stdout = subprocess.PIPE)
stdout, stderr = p.communicate()
print (p.returncode) # is 0 if success
mnemonic = os.getenv('MNEMONIC')
print(mnemonic)


# create a function for derive wallet
def derive_wallets(mnemonic,coin,numderive):
    command = f'./derive -g --mnemonic="{mnemonic}" --col=path,address,privkey,pubkey,pubkeyhash, --coin="{coin}" --numderive="{numderive}" --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys 


# test the function 
derive_wallets(mnemonic,ETH,3)


# Create an object
coins = {ETH: derive_wallets(mnemonic,ETH,3),
        BTCTEST:  derive_wallets(mnemonic,BTCTEST,3)}


# test the object
coins[ETH][0]['privkey']


# create a function that convert the privkey string in a child key to an account object.
def priv_key_to_account (coin, privkey):
    if coin == ETH:
        return Account.privateKeyToAccount(privkey)
    if coin == BTCTEST:
        return PrivateKeyTestnet(privkey)
    
    
# test the function  
priv_key_to_account(ETH,coins[ETH][0]['privkey']
                    

# create function for raw transaction 
def create_tx (coin, to, account, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "ChainID": w3.eth.chainId,
        }
    
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


# create a function to send transaction    
def send_tx (coin, account, to, amount):
    if coin == ETH:
        tx = create_tx(coin, to, account, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    
    if coin == BTCTEST:
        tx = create_tx(coin, to, account, amount)
        signed_tx = account.sign_transaction(tx)
        return NetworkAPI.broadcast_tx_testnet(signed)