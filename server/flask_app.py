import json
import logging
import random
import traceback
from datetime import datetime

from flask import Flask, Response, jsonify, make_response, render_template, request
from flask_cors import CORS
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException

from datamodel.models.payments import Transaction
from datamodel.models.userinfo import BankAccount, BillingInfo, CreditCard, DebitCard, Merchant, UserInfo
from db_queries import session
from helpers.user_management import check_userinfo, create_new_user, user_login, user_logout
from helpers.validator import user_exists, validate_transaction

app = Flask(
    __name__,
    static_folder="./client",
    template_folder="./client",
    # static_url_path="",
)


api_url = "/v1/"
payment_route = f"{api_url}payment"
CORS(app)

if __name__ != "__main__":
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.INFO)


@app.errorhandler(Exception)
def resource_not_found(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    try:
        error_object = {
            "error": {"status_code": code, "message": str(e).split(":", 1)[1].strip()}
        }
    except Exception as error:
        app.logger.info("Failed to parse the error message - {}".format(str(error)))
        error_object = e
    app.logger.info(
        "username - {}. This is the value of error object - {}".format(
            request.headers.get("X-Remote-User"), error_object
        )
    )
    return make_response(jsonify(error_object), code)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")


@app.route(api_url + "/get_current_time")
def get_current_time():
    return {
        "status": "Welcome - {}\nFull name - {} {}".format(
            request.headers.get("X-Remote-User"),
            request.headers.get("X-Firstname"),
            request.headers.get("-Lastname"),
        ),
        "message": "This is the default API endpoint",
    }


@app.route(api_url + "/users/get/<user_id>", methods=["GET"])
def get_user_info(user_id):
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        return jsonify(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": user.mobile_number,
                "email": user.email_id,
                "is_merchant": user.is_merchant,
                "created_on": user.created_on,
                "created_by": user.created_by,
                "updated_on": user.updated_on,
                "updated_by": user.updated_by,
            }
        )
    else:
        return make_response(jsonify({"message": "User not found"}), 404)


@app.route(api_url + "/users/create", methods=["POST"])
def create_users():
    data = request.get_json()    
    try:
        user_info = session.query(UserInfo).filter(UserInfo.user_name == data["user_name"]).first()
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "user does not exist"}), 404)

    if user_info is None:
        return make_response(jsonify({"message": "user does not exist"}), 404)

    user_info.first_name = data["first_name"]
    user_info.last_name = data["last_name"]
    user_info.mobile_number = data["mobile_number"]
    user_info.email_id = data["email_id"]
    user_info.is_merchant = data["is_merchant"]
    user_info.created_on = datetime.now()
    user_info.created_by = data["user_name"]
    user_info.updated_on = datetime.now()
    user_info.updated_by = data["user_name"]
    session.commit()

    if data["is_merchant"]:
        for merchant_info in data["merchant_info"]:
            merchant = Merchant(merchant_name=merchant_info["name"], category=merchant_info["category"], 
                                sub_category=merchant_info["sub_category"], user_id=user_info.user_id)
            session.add(merchant)
        session.commit()
        return make_response(jsonify({"message": "User created successfully", "id": user_info.user_id, "merchant_id": merchant.merchant_id}), 200)
    
    return make_response(jsonify({"message": "User created successfully", "id": user_info.user_id}), 200)

# {
#         "username": profile["username"],
#         "password": fake.password(),
#         "first_name": fake.first_name(),
#         "last_name": fake.last_name(),
#         "email_id": profile["mail"],
#         "mobile_number": generate_phone_number(),
#         "is_merchant": True,
#         "merchant_info": [
#             {
#                 "name": "ABC LTd",
#                 "category": "Food",
#                 "sub_category": "groceries"
#             }
#         ]
#     }

# route to update user_info


@app.route(api_url + "/userinfo/update/<user_id>", methods=["PUT"])
def update_user_info(user_id):
    data = request.get_json()
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.mobile_number = data["mobile_number"]
        user.email_id = data["email_id"]
        user.updated_on = datetime.now()
        user.updated_by = user_id
        return jsonify(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": user.mobile_number,
                "email": user.email_id,
                "is_merchant": user.is_merchant,
                "created_on": user.created_on,
                "created_by": user.created_by,
                "updated_on": user.updated_on,
                "updated_by": user.updated_by,
            }
        )

    else:
        return make_response(jsonify({"message": "User not found"}), 404)


# route to delete user


@app.route(api_url + "/userinfo/delete/<user_id>", methods=["DELETE"])
def delete_user_info(user_id):
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        debitcard_count = session.query(DebitCard).filter_by(user_id=user_id).count()
        if debitcard_count > 0:
            session.query(DebitCard).filter_by(user_id=user_id).delete()
            session.commit()
        creditcard_count = session.query(CreditCard).filter_by(user_id=user_id).count()
        if creditcard_count > 0:
            session.query(CreditCard).filter_by(user_id=user_id).delete()
            session.commit()
        account_count = session.query(BankAccount).filter_by(user_id=user_id).count()
        if account_count > 0:
            session.query(BankAccount).filter_by(user_id=user_id).delete()
            session.commit()
        merchant_count = session.query(Merchant).filter_by(user_id=user_id).count()
        if merchant_count > 0:
            session.query(Merchant).filter_by(user_id=user_id).delete()
            session.commit()
        session.delete(user)
        session.commit()
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    else:
        return make_response(jsonify({"message": "User not found"}), 404)


base_route = f"{api_url}/auth"


@app.route(f"{base_route}/create", methods=["POST"])
def create_user():
    user_data = request.json

    # Add to userinfo table
    ui = UserInfo(user_name=user_data["username"])
    try:
        session.add(ui)
        new_user = create_new_user(user_data["username"], user_data["password"])
        if new_user is None:
            session.rollback()
            return make_response(jsonify({"message": "user already exists"}), 409)
    except Exception as e:
        print(traceback.format_exc())
        return make_response(jsonify({"message": "Server Error"}), 500)

    session.commit()

    response = make_response(jsonify({"message": "user created"}), 200)
    # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')    
    return response


@app.route(f"{base_route}/login", methods=["POST"])
def login():
    user_data = request.json

    if "username" not in user_data.keys() or "password" not in user_data.keys():
        return make_response(jsonify({"message": "username or password missing"}), 400)

    token = user_login(user_data["username"], user_data["password"])

    if token is None:
        return make_response(
            jsonify({"message": "username or password incorrect"}), 401
        )

    resp = make_response(jsonify({"message": "logged in successfully"}), 200)
    for key, value in token.items():
        resp.set_cookie(key, json.dumps(value))
    resp.set_cookie("auth_token", json.dumps(token))
    ui = session.query(UserInfo).filter_by(user_name=user_data["username"]).first()
    return {"token": token, "user_id": ui.user_id}

@app.route(f"{base_route}/logout", methods=["POST"])
def logout():
    token = request.cookies.get("refresh_token")
    if token is None:
        return make_response(jsonify({"message": "refresh_token not set"}), 401)

    user_logout(token)
    return jsonify({"message": "logged out"})


@app.route(f"{base_route}/userinfo")
def userinfo():
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token is None or refresh_token is None:
        return make_response(jsonify({"message": "access or refresh token empty"}), 401)

    auth_token = {"access_token": access_token, "refresh_token": refresh_token}
    token, userinfo = check_userinfo(auth_token)

    if userinfo is not None:
        resp = make_response(jsonify({"userinfo": userinfo}), 200)
        resp.set_cookie("auth_token", json.dumps(token))
        resp.set_cookie("access_token", json.dumps(token["access_token"]))
        resp.set_cookie("refresh_token", json.dumps(token["refresh_token"]))
        return resp

    return make_response(jsonify({"message": "Unauthorized"}), 403)

# @app.route(f"{payment_route}/get_all_payment_methods/", methods=["GET"])
# def get_all_payment_methods():
@app.route(f"{payment_route}/get_all_payment_methods/<user_id>", methods=["GET"])
def get_all_payment_methods(user_id):
    try:
        if user_exists(user_id):
            method_dict = {}

            # get all bank accounts
            bank_info = session.query(BankAccount).filter_by(user_id=user_id).all()
            if bank_info:
                for bank in bank_info:
                    method_dict[f"{bank.bank_name}_{bank.account_number[-4:]}"] = {
                        "id": bank.account_number,
                        "method": "bank",
                    }

            # get all credit cards
            credit_cards = session.query(CreditCard).filter_by(user_id=user_id).all()
            if credit_cards:
                for card in credit_cards:
                    method_dict[f"{card.card_network}_{card.card_number[-4:]}"] = {
                        "id": card.card_number,
                        "method": "credit",
                    }

            # get all debit cards
            debit_cards = session.query(DebitCard).filter_by(user_id=user_id).all()
            if debit_cards:
                for card in debit_cards:
                    method_dict[f"{card.card_network}_{card.card_number[-4:]}"] = {
                        "id": card.card_number,
                        "method": "debit",
                    }
            return make_response(
                jsonify({"status": "Success", "data": method_dict}), 200
            )

        else:
            return make_response(jsonify({"message": "User does not exists"}), 404)

    except Exception as ex:
        traceback.print_exc()
        return make_response(jsonify({"message": "Server Error"}), 500)


@app.route(f"{payment_route}/get_payee_list/<user_id>", methods=["GET"])
def get_payee_list(user_id):
    payee_dict = {}
    try:
    #     return {
    #     "status": "Success", 
    #     "data": {"first_last_123": "123", "first_last_234": "234", "first_last_345": "345"}
    # }
        users = session.query(UserInfo).filter(UserInfo.user_id!=user_id).all()
        for user in users:
            name = f"{user.first_name}_{user.last_name}"
            user_id = user.user_id
            payee_dict[f"{name}_{user_id}"] = user_id

        return make_response(jsonify({"status": "Success", "data": payee_dict}), 200)
    except Exception as ex:
        traceback.print_exc()
        return make_response(jsonify({"message": "Server Error"}), 500)

# @app.route(f"{payment_route}/get_sender_list", methods=["GET"])
# def get_sender_list():
#     # print authorization token from header
#     print(request.headers.get('Authorization'))
#     return {"status": "Success", "data": {"aishwarya123": "123", "hemanth234": "234", "namratha345": "345"}}


@app.route(f"{payment_route}/send", methods=["POST"])
@app.route(f"{payment_route}/send/<transaction_id>", methods=["POST"])
def make_payment(transaction_id=None):
    data = request.get_json()
    payer_id = data["payer_id"]
    payee_id = data["payee_id"]
    transaction_method = data["transaction_method"]
    transaction_method_id = data["transaction_method_id"]
    transaction_amount = data["transaction_amount"]
    merchant_id = data.get("merchant_id", None)

    try:
        # validate the input
        is_valid, err_resp = validate_transaction(data)
        if not is_valid:
            return make_response(jsonify(err_resp), 400)

        if not transaction_id:
            # create a new transaction
            transaction = Transaction(
                payer_id=payer_id,
                payee_id=payee_id,
                transaction_amount=transaction_amount,
                transaction_method=transaction_method,
                transaction_method_id=transaction_method_id,
                merchant_id=merchant_id,
                is_completed=True,
                created_on=datetime.now(),
                created_by=payer_id,
            )
            # add the transaction to the session
            session.add(transaction)
        else:  # @TODO verify if the transaction_id is correct and if it is already completed or not
            transaction = (
                session.query(Transaction)
                .filter_by(transaction_id=transaction_id)
                .first()
            )
            transaction.transaction_method = (transaction_method,)
            transaction.transaction_method_id = (transaction_method_id,)
            transaction.updated_on = datetime.now()
            transaction.updated_by = payer_id
            transaction.is_completed = True

        # update the balance/credit limit for payer
        if transaction_method == "bank":
            method = (
                session.query(BankAccount)
                .filter_by(account_number=transaction_method_id)
                .first()
            )
            method.account_balance -= float(transaction_amount)
        elif transaction_method == "credit":
            method = (
                session.query(CreditCard)
                .filter_by(card_number=transaction_method_id)
                .first()
            )
            method.credit_limit -= float(transaction_amount)
        else:
            method = (
                session.query(DebitCard)
                .filter_by(card_number=transaction_method_id)
                .first()
            )
            bank_detail = (
                session.query(BankAccount)
                .filter_by(account_number=method.bank_account_number)
                .first()
            )
            bank_detail.account_balance -= float(transaction_amount)

        # update the balance for payee
        bank = session.query(BankAccount).filter_by(user_id=payee_id).first() # @TODO handle scenario when user has multiple bank accounts
        bank.account_balance += float(transaction_amount)

        # commit the changes
        session.commit()

        if not transaction_id:
            transaction_id = transaction.transaction_id

        return make_response(jsonify({"message": "Transaction successful", "id": transaction_id}), 201)

    except Exception as ex:
        traceback.print_exc()
        make_response(jsonify({"message": "Server Error"}), 500)


@app.route(f"{payment_route}/request", methods=["POST"])
def request_payment():
    data = request.get_json()
    requestor_id = data["requestor_id"]
    sender_id = data["sender_id"]
    amount = data["transaction_amount"]

    try:
        if user_exists(requestor_id) and user_exists(sender_id):
            transaction = Transaction(
                payer_id=sender_id,
                payee_id=requestor_id,
                transaction_amount=amount,
                is_completed=False,
                created_on=datetime.now(),
                created_by=requestor_id,
            )
            session.add(transaction)
            session.commit()

            transaction_id = transaction.transaction_id
            return make_response(
                jsonify({"message": "Transaction Request successful", "id": transaction_id}), 201
            )

        else:
            return make_response(jsonify({"message": "User does not exists"}), 404)

    except Exception as ex:
        traceback.print_exc()
        make_response(jsonify({"message": "Server Error"}), 500)


@app.route(f"{payment_route}/pending_requests/<user_id>", methods=["GET"])
def get_pending_requests(user_id):
# @app.route(f"{payment_route}/pending_requests", methods=["GET"])
# def get_pending_requests():
    try:
        # return {
        #     "message": "Success", "data":[{
        #             "requestor_id": 123,
        #             "requestor_name": "First last",
        #             "transaction_amount": 1000,
        #             "transaction_id": 1234
        #         },
        #         {
        #             "requestor_id": 234,
        #             "requestor_name": "First last 2000",
        #             "transaction_amount": 2000,
        #             "transaction_id": 5678
        #         }]
        # }
        if not user_id:
            return make_response(jsonify({"message": "User-id is required"}), 400)
        if user_exists(user_id):
            requests = []
            transactions = (
                session.query(Transaction)
                .filter_by(payer_id=user_id, is_completed=False)
                .all()
            )
            for transaction in transactions:
                requestor_id = transaction.payee_id
                user = session.query(UserInfo).filter_by(user_id=requestor_id).first()
                payment = {
                    "requestor_id": requestor_id,
                    "requestor_name": f"{user.first_name} {user.last_name}",
                    "transaction_amount": transaction.transaction_amount,
                    "transaction_id": transaction.transaction_id,
                }
                requests.append(payment)

            return make_response(jsonify({"message": "Success", "data": requests}), 200)

        else:
            return make_response(jsonify({"message": "User does not exists"}), 404)

    except Exception as ex:
        traceback.print_exc()
        make_response(jsonify({"message": "Server Error"}), 500)


@app.route(f"{payment_route}/cancel_pending_request/<transaction_id>", methods=["DELETE"])
def cancel_pending_request(transaction_id):
    try:
        transaction_id_to_delete = session.query(Transaction).filter_by(transaction_id=transaction_id).first()
        if transaction_id_to_delete:
            session.delete(transaction_id_to_delete)
            session.commit()
            return make_response(
                jsonify({"result": "Transaction deleted successfully"}), 200
            )
        else:
            return make_response(jsonify({"message": "Unable to delete transaction"}), 404)
    except Exception as ex:
        traceback.print_exc()
        return make_response(jsonify({"message": "Unable to delete transaction"}), 404)

# @app.route(api_url + "/add_new_credit_card", methods=["POST"])
# def add_new_credit_card():
#     return {"status": "Success"}

# route to add debit card and billing details using input from user


@app.route(api_url + "/debitcard/add", methods=["POST"])
def add_new_debit_card():
    try:
        data = request.get_json()
        billing_address = data["billing_address"]
        postal_code = data["postal_code"]
        state = data["state"]
        city = data["city"]
        billingaddress = BillingInfo(
            billing_address=billing_address, postal_code=postal_code, state=state, city=city
        )
        session.add(billingaddress)
        session.commit()
        card_number = data["card_number"]
        user_id = data["user_id"]
        card_network = data["card_network"]
        cvv = data["cvv"]
        billing_info_id = billingaddress.billing_info_id
        a = (
            session.query(BankAccount)
            .filter_by(account_number=data["bank_account_number"])
            .count()
        )
        if a == 0:
            return jsonify({"message": "Incorrect Bank Account number"}, 404)
        bank_account_number = data["bank_account_number"]
        created_on = datetime.now()
        created_by = data["user_id"]
        updated_on = datetime.now()
        updated_by = data["user_id"]
        debitcard = DebitCard(
            user_id=user_id,
            card_number=card_number,
            card_network=card_network,
            cvv=cvv,
            billing_info_id=billing_info_id,
            bank_account_number=bank_account_number,
            created_on=created_on,
            created_by=created_by,
            updated_on=updated_on,
            updated_by=updated_by,
        )
        session.add(debitcard)
        session.commit()
        return make_response(
            jsonify({"message": "Debit card details added successfully"}), 200
        )
    except Exception as ex:
        traceback.print_exc()
        session.rollback()
        make_response(jsonify({"message": "Server Error"}), 500)
# route to delete debit card and billing details


@app.route(api_url + "/debitcard/delete/<card_number>", methods=["DELETE"])
def delete_debit_card(card_number):
    try:
        debitcard = session.query(DebitCard).filter_by(card_number=card_number).first()
        billing_info_id = debitcard.billing_info_id
        billingaddress = (
            session.query(BillingInfo).filter_by(billing_info_id=billing_info_id).first()
        )
        if debitcard:
            session.delete(debitcard)
            session.commit()
        # if billingaddress:
            session.delete(billingaddress)
            session.commit()

            return make_response(
                jsonify({"result": "Debit card deleted successfully"}), 200
            )
        else:
            return make_response(jsonify({"message": "Debit card not found"}), 404)
    except Exception as ex:
        traceback.print_exc()
        session.rollback()
        make_response(jsonify({"message": "Server Error"}), 500)

@app.route(api_url + "/creditcard/add", methods=["POST"])
def add_new_credit_card():
    try:
        billing_address = request.json.get("billing_address")
        postal_code = request.json.get("postal_code")
        state = request.json.get("state")
        city = request.json.get("city")
        billing_info = BillingInfo(
            billing_address=billing_address, postal_code=postal_code, state=state, city=city
        )
        session.add(billing_info)
        session.commit()
        billing_info_id = billing_info.billing_info_id
        card_number = request.json.get("card_number")
        user_id = request.json.get("user_id")
        card_network = request.json.get("card_network")
        cvv = request.json.get("cvv")
        credit_limit = random.randint(1000, 2000)
        created_by = user_id
        updated_by = user_id
        created_on = datetime.now()
        updated_on = datetime.now()
        credit_card = CreditCard(
            card_number=card_number,
            user_id=user_id,
            card_network=card_network,
            cvv=cvv,
            billing_info_id=billing_info_id,
            credit_limit=credit_limit,
            created_by=created_by,
            updated_by=updated_by,
            created_on=created_on,
            updated_on=updated_on,
        )

        session.add(credit_card)
        session.commit()
        return make_response(
            jsonify({"message": "Credit card details added successfully"}), 200
        )
    except Exception as ex:
        traceback.print_exc()
        session.rollback()
        make_response(jsonify({"message": "Server Error"}), 500)


@app.route(api_url + "/creditcard/delete/<card_number>", methods=["DELETE"])
def delete_credit_card(card_number):
    try:
        credit_card = session.query(CreditCard).filter_by(card_number=card_number).first()

        if credit_card:
            billing_info_id = credit_card.billing_info_id
            session.delete(credit_card)
            session.commit()

            billingaddress = (
                session.query(BillingInfo)
                .filter_by(billing_info_id=billing_info_id)
                .first()
            )
            if billingaddress:
                session.delete(billingaddress)
                session.commit()

            return make_response(
                jsonify({"result": "Credit card deleted successfully"}), 200
            )
        else:
            return make_response(jsonify({"message": "Credit card not found"}), 404)
    except Exception as ex:
        traceback.print_exc()
        session.rollback()
        make_response(jsonify({"message": "Server Error"}), 500)


#route to add bank account details using input from user

@app.route(api_url + "/bankaccount/add", methods=['POST'])
def add_new_bank_account():
    try:
        data = request.get_json()
        account_number = data['account_number']
        user_id = data['user_id']
        account_holders_name = data['account_holders_name']
        account_balance = random.randint(1000, 2000)
        bank_name = data['bank_name']
        routing_number = data['routing_number']
        created_on = datetime.now()
        created_by = data['user_id']
        updated_on = datetime.now()
        updated_by = data['user_id']
        bankaccount = BankAccount(user_id = user_id,account_number=account_number, account_holders_name =account_holders_name, account_balance=account_balance, bank_name =bank_name , routing_number=routing_number, created_on=created_on, created_by=created_by, updated_on=updated_on, updated_by=updated_by)
        session.add(bankaccount)
        session.commit()
        return make_response(jsonify({'message': 'Bank account details added successfully'}),200)
    except Exception as ex:
        traceback.print_exc()
        session.rollback()
        make_response(jsonify({"message": "Server Error"}), 500)

#route to delete bank account details

@app.route(api_url + "/users/<user_id>/transactions", methods=["GET"])
def get_transactions(user_id):
 args = request.args
 start_date = args.get("start_date", default="", type=str)
 end_date = args.get("end_date", default="", type=str)
 start_date = datetime.strptime(start_date, "%d%m%Y").date()
 end_date = datetime.strptime(end_date, "%d%m%Y").date()
 result = session.query(Transaction).filter_by(payer_id=user_id).filter(Transaction.created_on.between(start_date, end_date))
 response = []
 for r in result:
    response.append({
        'transaction_id': r.transaction_id,
        'payee_id': r.payee_id, 
        'transaction_amount': r.transaction_amount,
        'transaction_method': r.transaction_method,
        'transaction_method_id': r.transaction_method_id,
        'is_completed': r.is_completed,
        'created_on': r.created_on,
        'created_by': r.created_by,
        'updated_on': r.updated_on,
        'updated_by': r.updated_by
 })
 return make_response(jsonify({"payer_id": user_id, "transactions": response}),200)

@app.route(api_url + "/bankaccount/delete/<account_number>", methods=["DELETE"])
def delete_bank_account(account_number):
    try:
        bankaccount = session.query(BankAccount).filter_by(account_number=account_number).first()
        if bankaccount:
            session.delete(bankaccount)
            session.commit()    
            return make_response(jsonify({"result": "Bank Account deleted successfully"}),200)
        else:
            return make_response(jsonify({'message': 'Bank Account not found'}),404)
    except Exception as ex:
        traceback.print_exc()
        session.rollback()
        make_response(jsonify({"message": "Server Error"}), 500)

@app.before_request
def basic_authentication():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return Response()


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
