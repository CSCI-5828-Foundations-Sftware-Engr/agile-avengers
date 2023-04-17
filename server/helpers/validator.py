import traceback
import sys
import os

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./"))

from datamodel.models.userinfo import UserInfo, BankAccount, CreditCard, DebitCard


def validate_transaction(transaction_detail, db_session):
    payer_id = transaction_detail["payer_id"]
    payee_id = transaction_detail["payee_id"]
    transaction_amount = transaction_detail["transaction_amount"]
    transaction_method = transaction_detail["transaction_method"]
    transaction_method_id = transaction_detail["transaction_method_id"]

    try:
        # payer check
        err_resp = {}
        user = db_session.query(UserInfo).filter_by(user_id=payer_id).first()
        if not user:
            err_resp = {"message": "Payer does not exists"}
            return False, err_resp

        # payer check
        user = db_session.query(UserInfo).filter_by(user_id=payee_id).first()
        if not user:
            err_resp = {"message": "Payee does not exists"}
            return False, err_resp

        # payment method check
        if transaction_method == "bank":
            method = (
                db_session.query(BankAccount)
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
                db_session.query(CreditCard)
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
                db_session.query(DebitCard)
                .filter_by(card_number=transaction_method_id)
                .first()
            )
            if not method:
                err_resp = {
                    "message": "Transaction method is incorrect. No corresponding debit card account found."
                }
                return False, err_resp
            bank_detail = (
                db_session.query(BankAccount)
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


def user_exists(user_id, db_session):
    user = db_session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        return True
    return False
