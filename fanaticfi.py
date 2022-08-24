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

celebrity_database = {
    "BILLYG": ["6 pack Bill", "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0", 6, 66666666666, "pics/bill.jpeg"],
    "ELON": ["Get lit with Elon Musk", "0x2422858F9C4480c2724A309D58Ffd7Ac8bF65396", 42, 42000000000420, "pics/elon.jpeg"],
    "TRUMP": ["Save Donald Trump", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 9, 9999999999999, "pics/trump.jpeg"],
    "KIMCHI": ["Kim owns all blockchains", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 11, 11111111111111, "pics/kim.jpeg"]
}
db_list = list(celebrity_database.values())


# A list of public figures' token names
token_names = ["BILLYG", "ELON", "TRUMP", "KIMCHI"]


def get_people(w3):
    """Display the database of Fintech Finders candidate information."""
    count=0
    max_cols=2
    max_rows=math.ceil(len(token_names)/max_cols)
    for each_row in range(max_rows):
        columns=st.columns(max_cols)
        for each_col in range(max_cols):
            if count <= len(token_names):
                with columns[each_col]:
                    st.image(db_list[count][4], width=250)
                    st.write("#### Name: ", db_list[count][0])
                    st.write("Ethereum Account Address: ", db_list[count][1])
                    st.write("#### Token Price: ", db_list[count][2], "ETH per token")
                    st.write("#### Only ", db_list[count][3], "amount of tokens are available")
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
account = generate_account()

# Write investor Ethereum account address and ballance to the sidebar
st.sidebar.markdown("## My account and balance")
st.sidebar.write(account.address)
st.sidebar.write(get_balance(w3, account.address), "ETH")

#Allow investors to select tokens to invest
person = st.sidebar.selectbox('Select Token to Invest', token_names)
number_of_tokens = st.sidebar.number_input("Number of Tokens Purchasing", step = 1)

st.sidebar.markdown("## Token Name, Token Price, and Ethereum Address")


# Identify the public figure that investing to
celebrity = celebrity_database[person][0]

# Write the Fintech Finder candidate's name to the sidebar
st.sidebar.write(celebrity)

# Clarify token price of selected celebrity
token_price = celebrity_database[person][2]

# Write the token price of selected celebrity to the sidebar
st.sidebar.write(token_price)

# Identify selected celebrity's Ethereum Address
celebrity_address = celebrity_database[person][1]

# Write selected celebrity's Ethereum Address to the sidebar
st.sidebar.write(celebrity_address)

# Write total cost of tokens
st.sidebar.markdown("## Total Token Cost in Ether")
total_cost = token_price * number_of_tokens
st.sidebar.write(total_cost)

# celebrity_database = {
#     "BILLYG": ["6 pack Bill", "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0", 6, 66666666666, "pics/bill.jpeg"],
#     "ELON": ["Get lit with Elon Musk", "0x2422858F9C4480c2724A309D58Ffd7Ac8bF65396", 42, 42000000000420, "pics/elon.jpeg"],
#     "TRUMP": ["Save Donald Trump", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 9, 9999999999999, "pics/trump.jpeg"],
#     "KIMCHI": ["Kim owns all blockchains", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", 11, 11111111111111, "pics/kim.jpeg"]
# }
# db_list = list(celebrity_database.values())
if st.sidebar.button("Buy Token"):
    for i in db_list:
        transaction_hash = send_transaction(w3, account, i[1], i[2]*number_of_tokens)
        
        # Update total number of tokens
        db_list[db_list.index(i)][3] = i[3] - number_of_tokens

        # Markdown for the transaction hash
        st.sidebar.markdown("#### Validated Transaction Hash")

        # Write the returned transaction hash to the screen
        st.sidebar.write(transaction_hash)

        # Celebrate your successful payment
        st.balloons()

        


get_people(w3)