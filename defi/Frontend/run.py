from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField
from brownie import accounts, Contract, network
from dotenv import load_dotenv
import os
load_dotenv()



app=Flask(__name__)
app.config['SECRET_KEY']="terimammimerihoja420420"

network.connect('rinkeby')


usdcAddress=Contract("0x6bd724AF600D5CCC313Dac0BA6B96dCed1C07F6d")
defi_contract=Contract("0xaF5AA075cb327d83cB8D565D95202494569517a9")
account=accounts.add(os.getenv("PRIVATE_KEY"))
account=accounts.add(os.getenv("PRIVATE_KEY1"))

account=accounts.add(os.getenv("PRIVATE_KEY2"))





class Form(FlaskForm):
    Faccounts=SelectField('Account', choices=['0xCDF770392F1E5E61725Cc9522c80070134D50eC7', 
                                                '0x37A138b583cD2d740B8020BDbf61C39E90a8063F',
                                                '0x79472239719B2D2Db1944C32ec0Fa6Db4a746513' ])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposit')
def deposit():
    form =Form()
    AvailableBal=SC_getAccountbal()/10**18
    DepositedAmount= defi_contract.depositBalance(account)/(10**18)
    return render_template('deposit.html', form=form, AvailableBal=AvailableBal, DepositedAmount=DepositedAmount)



@app.route('/depositButton', methods=['GET', 'POST'])
def depositButton():
    form=Form()
    if request.method=='POST':
        depositAmount=request.form.get("depositValue", type=int)*(10**18)
        SC_depositBal(depositAmount)
        DepositedAmount= defi_contract.depositBalance(account)/(10**18)
        AvailableBal=usdcAddress.balanceOf(account)/(10**18)
    return render_template('deposit.html',form=form, AvailableBal=AvailableBal,DepositedAmount=DepositedAmount)


@app.route('/withdrawButton', methods=['GET', 'POST'])
def withdrawButton():
    form=Form()
    if request.method=='POST':
        withdrawAmount=request.form.get("withdrawValue", type=int)*(10**18)
        SC_withdrawBal(withdrawAmount)
        DepositedAmount= defi_contract.depositBalance(account)/(10**18)
        AvailableBal=usdcAddress.balanceOf(account)/(10**18)
    return render_template('deposit.html',form=form, AvailableBal=AvailableBal,DepositedAmount=DepositedAmount)

def SC_withdrawBal(withdrawAmount):
    defi_contract.withdraw(withdrawAmount, {"from":account})


def SC_getAccountbal():
    balance=usdcAddress.balanceOf(account)
    return balance

def SC_depositBal(depositAmount):
    usdcAddress.approve(defi_contract, depositAmount, {"from":account})
    defi_contract.depositToken(depositAmount, {"from":account})

@app.route('/refresh/<currentAccount>')
def refresh(currentAccount):
    global account
    account=accounts.at(currentAccount)
    currentBal=usdcAddress.balanceOf(account)/(10**18)
    stakedBalance=defi_contract.depositBalance(account)/(10**18)
    return jsonify({'response':currentAccount, 'stakedBalance':stakedBalance, 'currentBal':currentBal})

@app.route('/FundMe', methods=["GET", "POST"])
def FundMe():
    if request.method=="POST":
        FromAddress=request.form.get("fromAddress")
        FromAddress=accounts.at(FromAddress, force=True)
        ToAddress=request.form.get("toAddress") 
        Amount=request.form.get("Amount", type=int)
        usdcAddress.transfer(ToAddress, Amount*10**18, {"from": FromAddress})
    return render_template('FundMe.html')


if __name__=="__main__":
    app.run()
    network.disconnect()