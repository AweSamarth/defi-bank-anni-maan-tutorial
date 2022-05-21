import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    account=accounts.add(os.getenv("PRIVATE_KEY"))
    usdc_contract=Contract("0x6bd724AF600D5CCC313Dac0BA6B96dCed1C07F6d")
    defi_contract=Contract("0xaF5AA075cb327d83cB8D565D95202494569517a9")
    print(f"Before usdc token balance is{defi_contract.depositBalance(account)}")
    usdc_contract.approve(defi_contract, 10000, {"from":account})
    defi_contract.depositToken(10000, {"from":account})


    print(f"Current usdc token balance is {defi_contract.depositBalance(account)}")
    
    
    defi_contract.withdraw(100, {"from":account})


    print(f"balance after withdrawing is {defi_contract.depositBalance(account)}")