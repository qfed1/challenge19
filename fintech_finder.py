# Cryptocurrency Wallet

################################################################################
# For this Challenge, you will assume the perspective of a Fintech Finder
# customer in order to do the following:

# * Generate a new Ethereum account instance by using your mnemonic seed phrase
# (which you created earlier in the module).

# * Fetch and display the account balance associated with your Ethereum account
# address.

# * Calculate the total value of an Ethereum transaction, including the gas
# estimate, that pays a Fintech Finder candidate for their work.

# * Digitally sign a transaction that pays a Fintech Finder candidate, and send
# this transaction to the Ganache blockchain.

# * Review the transaction hash code associated with the validated blockchain transaction.

# Once you receive the transaction’s hash code, you will navigate to the Transactions
# section of Ganache to review the blockchain transaction details. To confirm that
# you have successfully created the transaction, you will save screenshots to the
# README.md file of your GitHub repository for this Challenge assignment.

################################################################################
# Imports
import os
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
from dotenv import load_dotenv
from web3 import Web3
from web3.auto.infura import w3
from web3.middleware import geth_poa_middleware
from pathlib import Path
from eth_account import Account
from crypto_wallet import generate_account, get_balance, send_transaction

load_dotenv()
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
mnemonic = os.getenv("MNEMONIC")

################################################################################
# Step 1 - Part 3:
# Import the following functions from the `crypto_wallet.py` file:
# * `generate_account`
# * `get_balance`
# * `send_transaction`

def generate_account(mnemonic):
    return Account.from_mnemonic(mnemonic)

def get_balance(address):
    return w3.eth.getBalance(address)

def send_transaction(account, to, value):
    gasEstimate = w3.eth.estimateGas({"from": account.address, "to": to, "value": value})
    transaction = {
        "from": account.address,
        "to": to,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": w3.eth.gasPrice,
        "nonce": w3.eth.getTransactionCount(account.address),
    }
    signed_txn = account.signTransaction(transaction)
    return w3.eth.sendRawTransaction(signed_txn.rawTransaction)

################################################################################
# Fintech Finder Candidate Information

# Database of Fintech Finder candidates including their name, digital address, rating and hourly cost per Ether.
# A single Ether is currently valued at $1,500
candidate_database = {
    "Lane": ["Lane", "0xaC8eB8B2ed5C4a0fC41a84Ee4950F417f67029F0", "4.3", .20, "Images/lane.jpeg"],
    "Ash": ["Ash", "0x2422858F9C4480c2724A309D58Ffd7Ac8bF65396", "5.0", .33, "Images/ash.jpeg"],
    "Jo": ["Jo", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.7", .19, "Images/jo.jpeg"],
    "Kendall": ["Kendall", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.7", .25, "Images/kendall.jpeg"],
    "Skye": ["Skye", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.5", .22, "Images/skye.jpeg"],
    "Robin": ["Robin", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45", "4.2", .15, "Images/robin.jpeg"],
}

################################################################################
# Streamlit Code

st.set_page_config(
    page_title="Fintech Finder",
    page_icon=":money_with_wings:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Fintech Finder")
st.sidebar.title("Menu")

account = generate_account(mnemonic)
eth_balance = get_balance(account.address)

st.sidebar.image("Images/user_image.jpg", width=200)
st.sidebar.markdown(f"### {account.address}")
st.sidebar.markdown(f"### {eth_balance} Wei")

candidate = st.sidebar.radio("Select a Candidate", list(candidate_database.keys()))

selected_candidate = candidate_database[candidate]
st.image(selected_candidate[4], width=300)
st.write(f"**Name:** {selected_candidate[0]}")
st.write(f"**Rating:** {selected_candidate[2]} stars")
st.write(f"**Hourly cost per Ether:** {selected_candidate[3]} Ether")

hours = st.slider("Select hours worked", 1, 10, 1)
total_cost = selected_candidate[3] * hours
total_cost_wei = int(total_cost * 1e18)
total_value = total_cost * 1500

if st.button("Pay Candidate"):
    txn_hash = send_transaction(account, selected_candidate[1], total_cost_wei)
    st.success(f"Transaction sent! Transaction hash: {txn_hash.hex()}")
    st.balloons()
