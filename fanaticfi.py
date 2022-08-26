# Imports
import os
import json
import math
import time
from web3 import Web3
import streamlit as st
# from typing import Any, List
# from dotenv import load_dotenv
# from dataclasses import dataclass
from investor_wallet import generate_account, get_balance, send_transaction

w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))

with open("BillGates_abi.json") as token_abi:
    BillGates_abi = json.load(token_abi)
with open("BillGates_Crowdsale_abi.json") as crowdsale_abi:
    BillGates_Crowdsale_abi = json.load(crowdsale_abi)
with open("BillGates_deployer_abi.json") as deployer_abi:
    BillGates_deployer_abi = json.load(deployer_abi)

token_contract=w3.eth.contract(address='0xd2A968111493720C9648C3A65e065763a3a636E7', abi=BillGates_abi)
crowdsale_contract=w3.eth.contract(address='0xD437b73bd1A35ab9557ad20423aB19371EE40174', abi=BillGates_Crowdsale_abi)
deployer_contract=w3.eth.contract(address='0x6aDc86a713a27bEDFD5FADCD99C23918541527D6', abi=BillGates_deployer_abi)


celebrity_database = {
    "BILLYG": ["6 pack Bill", "0x6aDc86a713a27bEDFD5FADCD99C23918541527D6", 6, "pics/bill.jpeg"],
    "ELON": ["Get lit with Elon Musk", "0x2422858F9C4480c2724A309D58Ffd7Ac8bF65396", 42, "pics/elon.jpeg"],
    "TRUMP": ["Save Donald Trump", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 9, "pics/trump.jpeg"],
    "KIMCHI": ["Kim owns all blockchains", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 11, "pics/kim.jpeg"]
}
db_list = list(celebrity_database.values())


# A list of public figures' token names
token_names = ["BILLYG", "ELON", "TRUMP", "KIMCHI"]


def get_people(w3):
    """Display the database of celebrities and their tokens information."""
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


# Streamlit application headings
col1, col2 = st.columns((1,2))

with col1:
    st.image("pics/fanaticfi.jpeg", width=150)
    st.text(" \n")
with col2:
    st.title("Welcome to FanaticFi!")
    st.header("WHERE FANS GET TO DECIDE!")
    st.text(" \n")


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

# Click button to make transaction
if st.sidebar.button("Buy Token"):
    
    transaction_hash = send_transaction(w3, investor_account, celebrity_address, total_cost)

    for token_name in token_names:

        # Write available token balance
        num_token=token_contract.functions.balanceOf(celebrity_database[token_name][1]).call()
        st.sidebar.write("#### Only ", num_token, "amount of tokens are available")

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()

        

get_people(w3)