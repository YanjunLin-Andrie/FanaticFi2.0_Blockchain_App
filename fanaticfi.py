# Imports
import json
import math
from web3 import Web3
import streamlit as st
from investor_wallet import generate_account, get_balance, buy_token

#----------------------------------------------------------------------------------------------------------------------
# Preparations 
#----------------------------------------------------------------------------------------------------------------------

# Link app with ganache
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))

# Load all abi files

# abi_database = {
#                 "BillGates_abis": ["abi_files/BillGates_abi.json", "token_abi","BillGates_abi",
#                 "abi_files/BillGates_Crowdsale_abi.json", "crowdsale_abi", "BillGates_Crowdsale_abi",
#                 "abi_files/BillGates_deployer_abi.json", "deployer_abi", "BillGates_deployer_abi"]
# }
# abi_db_list = list(abi_database.values())

# abi_owners = ["BillGates_abis"]

# with open(abi_database[abi_owners][0]) as abi_database[abi_owners][1]:
#     abi_database[abi_owners][2] = json.load(abi_database[abi_owners][1])
# with open(abi_database[abi_owners][3]) as abi_database[abi_owners][4]:
#     abi_database[abi_owners][5] = json.load(abi_database[abi_owners][4])
# with open(abi_database[abi_owners][6]) as abi_database[abi_owners][7]:
#     abi_database[abi_owners][8] = json.load(abi_database[abi_owners][7])

#########
######### The method above was attemp to keep the code DRY, but we realized the unhashable list error. Below method is our final choice.
#########

with open("abi_files/BillGates_abi.json") as token_abi:
    BillGates_abi = json.load(token_abi)
with open("abi_files/BillGates_Crowdsale_abi.json") as crowdsale_abi:
    BillGates_Crowdsale_abi = json.load(crowdsale_abi)
with open("abi_files/BillGates_deployer_abi.json") as deployer_abi:
    BillGates_deployer_abi = json.load(deployer_abi)

with open("abi_files/ElonMusk_abi.json") as elon_token_abi:
    ElonMusk_abi = json.load(elon_token_abi)
with open("abi_files/ElonMusk_Crowdsale_abi.json") as elon_crowdsale_abi:
    ElonMusk_Crowdsale_abi = json.load(elon_crowdsale_abi)
with open("abi_files/ElonMusk_deployer_abi.json") as elon_deployer_abi:
    ElonMusk_deployer_abi = json.load(elon_deployer_abi)

with open("abi_files/DonaldTrump_abi.json") as trump_token_abi:
    DonaldTrump_abi = json.load(trump_token_abi)
with open("abi_files/DonaldTrump_Crowdsale_abi.json") as trump_crowdsale_abi:
    DonaldTrump_Crowdsale_abi = json.load(trump_crowdsale_abi)
with open("abi_files/DonaldTrump_deployer_abi.json") as trump_deployer_abi:
    DonaldTrump_deployer_abi = json.load(trump_deployer_abi)

with open("abi_files/Kimchi_abi.json") as kim_token_abi:
    Kimchi_abi = json.load(kim_token_abi)
with open("abi_files/Kimchi_Crowdsale_abi.json") as kim_crowdsale_abi:
    Kimchi_Crowdsale_abi = json.load(kim_crowdsale_abi)
with open("abi_files/Kimchi_deployer_abi.json") as kim_deployer_abi:
    Kimchi_deployer_abi = json.load(kim_deployer_abi)

# Establish celebrity database
celebrity_database = {
    "BILLYG": ["6 pack Bill", "0xa9Cb436660CA86a6f1955Feb079C5066d6A91cB0", 0.66, "pics/bill.jpeg", 
    '0xF951439Aa8FCAE61c7FaEf7aD9B923e3513E92df', '0x5BC5F75baC7F2c057efaec82f8102F31526bA47d', BillGates_deployer_abi,
    BillGates_Crowdsale_abi, BillGates_abi],

    "ELON": ["Get lit with Elon Musk", "0xd9BA61598720508C1A7FCC403EA87E6de762e0C6", 0.42, "pics/elon.jpeg",
    '0xDfE15b50803748BB523df696a972E2bCd12C0d2f', '0x3F62D19Db825A0aa73A491239E3e41dF46BbdafE', ElonMusk_deployer_abi,
    ElonMusk_Crowdsale_abi, ElonMusk_abi],

    "TRUMP": ["Save Donald Trump", "0x0E68C98676DbEfE6A1a53e304E8D0FA8027Fa122", 0.99, "pics/trump.jpeg",
    '0xaba4711771e0B7AFC30237F3D3E41876B9D64538', '0xf7D5201Aa9Ed749A8573BcdF7D89b53534B394EB', DonaldTrump_deployer_abi,
    DonaldTrump_Crowdsale_abi, DonaldTrump_abi],

    "KIMCHI": ["Kim owns all blockchains", "0x28CF16cd57cb03AA25B3A8a7F4e4eA25A778D385", 0.11, "pics/kim.jpeg",
    '0x583cfC469CcF2a14bc8B77b1740a6b2333E6F721','0xD86f7e5fECA055e6B3B5d93C9Dc6EEC0C95097d7', Kimchi_deployer_abi,
    Kimchi_Crowdsale_abi, Kimchi_abi]
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

    transaction_hash = buy_token(w3, investor_account, celebrity_address, total_cost)

    # Calculate remaining number of tokens available for sale
    total_supply = token_contract.functions.totalSupply().call()
    cap = crowdsale_contract.functions.cap().call()
    remaining_tokens = cap - total_supply

    # Write available token balance
    st.sidebar.write("#### Only ", remaining_tokens, "amount of tokens are available")

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()

get_people(w3)