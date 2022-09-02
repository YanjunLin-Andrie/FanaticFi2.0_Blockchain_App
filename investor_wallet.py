# Imports
import os
from web3 import Account
from bip44 import Wallet
from dotenv import load_dotenv
# from fanaticfi import crowdsale_contract
# from web3.gas_strategies.time_based import medium_gas_price_strategy
load_dotenv('sample.env')

################################################################################
# Wallet functionality


def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    mnemonic = os.getenv("MNEMONIC")

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    return account


def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


# def send_transaction(w3, account, to, token_price):
#     """Send an authorized transaction to the Ganache blockchain."""
#     # Set gas price strategy
#     w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

#     # Convert eth amount to Wei
#     value = w3.toWei(token_price, "ether")

#     # Calculate gas estimate
#     gasEstimate = w3.eth.estimateGas(
#         {"to": to, "from": account.address, "value": value})

#     # Construct a raw transaction
#     raw_tx = {
#         "to": to,
#         "from": account.address,
#         "value": value,
#         "gas": gasEstimate,
#         "gasPrice": 0,
#         "nonce": w3.eth.getTransactionCount(account.address)
#     }

#     # Sign the raw transaction with ethereum account
#     signed_tx = account.signTransaction(raw_tx)

#     # Send the signed transactions
#     return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

# def buy_token(w3, account, beneficiary, token_price):
#     # Set gas price strategy
#     w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

#     # Convert eth amount to Wei
#     value = w3.toWei(token_price, "ether")

#     # Calculate gas estimate
#     gasEstimate = w3.eth.estimateGas(
#         {"from": account.address, "value": value})
#     # Construct a raw transaction
#     txn={
#         'from': account.address,
#         'value': value, 
#         'gas': gasEstimate,
#         'gasPrice': 0,
#         'nonce': w3.eth.get_transaction_count(account.address)
#         }

#     # Sign the raw transaction with ethereum account
#     signed_txn=account.signTransaction(txn)


#     # crowdsale_contract.functions.buyTokens(beneficiary).buildTransaction()

#     # Send the signed transactions
#     return w3.eth.sendRawTransaction(signed_txn.rawTransaction)
