# Imports
# import os
import json
import math
# import time
from web3 import Web3
import streamlit as st
# from typing import Any, List
# from dotenv import load_dotenv
# from dataclasses import dataclass
from investor_wallet import generate_account, get_balance, send_transaction

#----------------------------------------------------------------------------------------------------------------------
# Preparations 
#----------------------------------------------------------------------------------------------------------------------

# Link app with ganache
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))

##### ? Ways to simplify?
# Load all abi files
with open("BillGates_abi.json") as token_abi:
    BillGates_abi = json.load(token_abi)
with open("BillGates_Crowdsale_abi.json") as crowdsale_abi:
    BillGates_Crowdsale_abi = json.load(crowdsale_abi)
with open("BillGates_deployer_abi.json") as deployer_abi:
    BillGates_deployer_abi = json.load(deployer_abi)

with open("ElonMusk_abi.json") as elon_token_abi:
    ElonMusk_abi = json.load(elon_token_abi)
with open("ElonMusk_Crowdsale_abi.json") as elon_crowdsale_abi:
    ElonMusk_Crowdsale_abi = json.load(elon_crowdsale_abi)
with open("ElonMusk_deployer_abi.json") as elon_deployer_abi:
    ElonMusk_deployer_abi = json.load(elon_deployer_abi)

# elon_token_contract=w3.eth.contract(address='0x64FD6fd4fDca000d02E4D4402C25f1eb040F66E0', abi=ElonMusk_abi)
# elon_crowdsale_contract=w3.eth.contract(address='0xd6DE0A378D08336978aDD6b7610D4FA0678b1c22', abi=ElonMusk_Crowdsale_abi)
# elon_deployer_contract=w3.eth.contract(address='0xC85F6D26612D4B82F0A87F426772755BECBE34d9', abi=ElonMusk_deployer_abi)

celebrity_database = {
    "BILLYG": ["6 pack Bill", "0xc215a18c75Cc940c8ec534Cdfd8aE9029B966120", 0.66, "pics/bill.jpeg", 
    '0xb5bb93eACfc127f3BC0E507d77D481c2317797B0', '0x32aFA87964CC2bA46f4396104F43EFdcCDd2DC44', BillGates_deployer_abi,
    BillGates_Crowdsale_abi, BillGates_abi],

    "ELON": ["Get lit with Elon Musk", "0xC85F6D26612D4B82F0A87F426772755BECBE34d9", 0.42, "pics/elon.jpeg",
    '0xd6DE0A378D08336978aDD6b7610D4FA0678b1c22', '0x64FD6fd4fDca000d02E4D4402C25f1eb040F66E0', ElonMusk_deployer_abi,
    ElonMusk_Crowdsale_abi, ElonMusk_abi],

    "TRUMP": ["Save Donald Trump", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 0.99, "pics/trump.jpeg"],
    "KIMCHI": ["Kim owns all blockchains", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 0.11, "pics/kim.jpeg"]
}
db_list = list(celebrity_database.values())

# A list of public figures' token names
token_names = ["BILLYG", "ELON", "TRUMP", "KIMCHI"]

#----------------------------------------------------------------------------------------------------------------------
# Main page functions and designs
#----------------------------------------------------------------------------------------------------------------------

# Streamlit application headings
col1, col2 = st.columns((1,2))

with col1:
    st.image("pics/fanaticfi.jpeg", width=150)
    st.text(" \n")
with col2:
    st.title("Welcome to FanaticFi!")
    st.header("WHERE FANS GET TO DECIDE!")
    st.text(" \n")

# Display the database of celebrities and their tokens information
def get_people(w3):
    count=0
    max_cols=2
    max_rows=math.ceil(len(token_names)/max_cols)
    
    for each_row in range(max_rows):
        columns=st.columns(max_cols)
        for each_col in range(max_cols):
            if count <= len(token_names):
                with columns[each_col]:
                    st.image(db_list[count][3], width=250)
                    st.write("#### ", db_list[count][0])
                    st.write("Ethereum Account Address: ", db_list[count][1])
                    st.write("#### Token Price: ", db_list[count][2], "ETH per token")
                    st.text(" \n")
                    count +=1

#----------------------------------------------------------------------------------------------------------------------
# Sidebar functions and designs
#----------------------------------------------------------------------------------------------------------------------

st.sidebar.markdown("## Purchase Celebrity Tokens HERE!")

# Allow investors to create an account to buy tokens
investor_account = generate_account()

# Write investor Ethereum account address and ballance to the sidebar
st.sidebar.markdown("## My account and balance")
st.sidebar.write(investor_account.address)
st.sidebar.write(get_balance(w3, investor_account.address), "ETH")

#Allow investors to select tokens to invest
token_name = st.sidebar.selectbox('Select Token to Invest', token_names)

number_of_tokens = st.sidebar.number_input("Number of Tokens Purchasing", step = 1)

st.sidebar.write('---')
st.sidebar.markdown("## Token Name, Token Price, and Celebrity Ethereum Address")

# Identify the public figure that investing to
celebrity = celebrity_database[token_name][0]

# Write the Fintech Finder candidate's name to the sidebar
st.sidebar.write(celebrity)

# Clarify token price of selected celebrity
token_price = celebrity_database[token_name][2]

# Write the token price of selected celebrity to the sidebar
st.sidebar.write(token_price)

# Identify selected celebrity's Ethereum Address
celebrity_address = celebrity_database[token_name][1]

# Write selected celebrity's Ethereum Address to the sidebar
st.sidebar.write(celebrity_address)

# Write total cost of tokens
st.sidebar.markdown("## Total Token Cost in Ether")
total_cost = token_price * number_of_tokens
st.sidebar.write(total_cost)

st.sidebar.write(celebrity_address)
st.sidebar.write(investor_account)

# Load deployer, crowdsale, and token contracts with abi files

deployer_contract=w3.eth.contract(address=celebrity_address, abi=celebrity_database[token_name][6])
crowdsale_contract=w3.eth.contract(address=celebrity_database[token_name][4], abi=celebrity_database[token_name][7])
token_contract=w3.eth.contract(address=celebrity_database[token_name][5], abi=celebrity_database[token_name][8])

#----------------------------------------------------------------------------------------------------------------------
# Transaction functionality designs
#----------------------------------------------------------------------------------------------------------------------

# Click button to buy tokens
if st.sidebar.button("Buy Token"):

    # Calculate gas estimate
    # gasEstimate = w3.eth.estimateGas(
    #     {"to": str(celebrity_address), "from": str(investor_account), "value": number_of_tokens})
    
    # raw_tx = {
    #     "from": str(investor_account),
    #     "value": number_of_tokens,
    #     "gas": gasEstimate,
    #     "gasPrice": 0,
    #     "nonce": w3.eth.getTransactionCount(investor_account)
    # }
    # Sign the raw transaction with ethereum account
    # signed_tx = investor_account.signTransaction(raw_tx)

    # crowdsale_contract.functions.buyTokens(raw_tx).send_transaction(w3, investor_account, celebrity_address, total_cost)
    
    

    transaction_hash = send_transaction(w3, investor_account, celebrity_address, total_cost)

    # Calculate remaining number of tokens available for sale
    total_supply = token_contract.functions.totalSupply().call()
    goal = crowdsale_contract.functions.goal().call()
    remaining_tokens = goal - total_supply

    # Write available token balance
    st.sidebar.write("#### Only ", remaining_tokens, "amount of tokens are available")

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()

get_people(w3)