from web3 import Web3
import schedule
import time
import os
from dotenv import load_dotenv

# Load privkey and rpc-url from .env
load_dotenv()

# --- PulseChain Node, Wallet, and Contract Addresses ---
PULSECHAIN_RPC_URL = os.getenv("PULSECHAIN_RPC_URL") # setup in .env, https://rpc.pulsechain.com is fine (for now)
PRIVATE_KEY = os.getenv("PRIVATE_KEY") # setup in .env (be careful of the risks, use a specific wallet for this, not your main one)
ORDERSIZE = os.getenv("ORDER_SIZE") #setup in the .env the amount of PLS you wish to use for each buy order
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")  # Target token which is also to be determined in the .env (Be part of the $FEW as a thank you!)
ROUTER_ADDRESS = "0xcf6402cdEdfF50Fe334471D0fDD33014E40e828c" # Pump.tires router
WPLS_ADDRESS = "0xA1077a294dDE1B09bB078844df40758a5D0f9a27" # WPLS address for conversion before transacting

# --- Minimal Router ABI to buy a token on pump.tires (more features are coming) ---
ROUTER_ABI = [
    {
        "inputs": [
            {"name": "paymentToken", "type": "address"},
            {"name": "payAmount", "type": "uint256"},
        ],
        "name": "buyTokenExactIn",
        "stateMutability": "payable",
        "type": "function",
    }
]

# --- Web3 Setup ---
w3 = Web3(Web3.HTTPProvider(PULSECHAIN_RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
ACCOUNT_ADDRESS = account.address

print(f"Connected: {w3.is_connected()}")
print(f"Account: {ACCOUNT_ADDRESS}")

# --- Get Chain ID ---
CHAIN_ID = w3.eth.chain_id
print(f"Chain ID: {CHAIN_ID}")

# --- Contract Instance ---
router_contract = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)

# --- Buy Token Function ---
def buy_token(amount_pls):
    try:
        pay_amount = w3.to_wei(amount_pls, 'ether')  # Convert PLS to its Wei counterpart

        encoded_data = router_contract.encode_abi(
            "buyTokenExactIn", [w3.to_checksum_address(TOKEN_ADDRESS), pay_amount]
        )

        transaction = {
            'from': ACCOUNT_ADDRESS,
            'to': ROUTER_ADDRESS,
            'value': pay_amount,  # Send the exact amount of PLS
            'gas': 350000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(ACCOUNT_ADDRESS),
            'data': encoded_data,
            'chainId': CHAIN_ID,
        }

        signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"Sent: {tx_hash.hex()}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Confirmed: {receipt}")
        return receipt

    except Exception as e:
        print(f"Error: {e}")
        return None

# --- Task Scheduling ---
def job():
    print("Running...")
    buy_token(ORDERSIZE)  # Buy using 20000 PLS - ADJUST AS NEEDED IN .ENV
job() # Do a buy as soon as the script is launched (COMMENT IF YOU DON'T WANT TO INSTABUY)
schedule.every().hour.do(job) # Do a buy every hour - ADJUST AS NEEDED, CFR README

while True:
    schedule.run_pending()
    time.sleep(60)
