import traceback
import sys
import os

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./"))

from datamodel.models.userinfo import UserInfo, BankAccount, CreditCard, DebitCard
from db_queries import session, engine

def validate_transaction(transaction_detail): # @TODO Add validation of credit/debit card only being used to pay to merchant
    payer_id = transaction_detail["payer_id"]
    payee_id = transaction_detail["payee_id"]
    transaction_amount = transaction_detail["transaction_amount"]
    transaction_method = transaction_detail["transaction_method"]
    transaction_method_id = transaction_detail["transaction_method_id"]

    try:
        # payer check
        err_resp = {}
        if not user_exists(payer_id):
            err_resp = {"message": "Payer does not exists"}
            return False, err_resp

        # payer check
        if not user_exists(payee_id):
            err_resp = {"message": "Payee does not exists"}
            return False, err_resp
    
        # self test
        if payer_id == payee_id: # @TODO is this test required?
            err_resp = {"message": "Can't transfer Money to self"}
            return False, err_resp

        # payment method check
        if transaction_method == "bank":
            method = (
                session.query(BankAccount)
                .filter_by(account_number=transaction_method_id)
                .first()
            )
            if not method:
                err_resp = {
                    "message": "Transaction method is incorrect. No corresponding bank account found."
                }
                return False, err_resp
            if method.account_balance - transaction_amount <= 0:
                err_resp = {
                    "message": "Insufficient funds, transaction cannot take place"
                }
        elif transaction_method == "credit":
            method = (
                session.query(CreditCard)
                .filter_by(card_number=transaction_method_id)
                .first()
            )
            if not method:
                err_resp = {
                    "message": "Transaction method is incorrect. No corresponding credit card account found."
                }
                return False, err_resp
            if method.credit_limit - transaction_amount <= 0:
                err_resp = {
                    "message": "Insufficient funds, transaction cannot take place"
                }
        elif transaction_method == "debit":
            method = (
                session.query(DebitCard)
                .filter_by(card_number=transaction_method_id)
                .first()
            )
            if not method:
                err_resp = {
                    "message": "Transaction method is incorrect. No corresponding debit card account found."
                }
                return False, err_resp
            bank_detail = (
                session.query(BankAccount)
                .filter_by(account_number=method.bank_account_number)
                .first()
            )
            if bank_detail.account_balance - transaction_amount <= 0:
                err_resp = {
                    "message": "Insufficient funds, transaction cannot take place"
                }
        else:
            err_resp = {
                "message": "Available transaction methods are bank, credit and debit card."
            }

        if err_resp:
            return False, err_resp
        return True, err_resp
    except Exception as ex:
        traceback.print_exc()
        return False, {"message": "Internal Server error."}


def user_exists(user_id):
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        return True
    return False
