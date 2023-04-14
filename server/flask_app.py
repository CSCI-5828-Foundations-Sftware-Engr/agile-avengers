import json
import logging
import os
import random
import socket
import string
import sys
import traceback
from datetime import datetime

# import sqlalchemy
import sqlalchemy as db
from flask import Flask, abort, jsonify, make_response, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import HTTPException

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./"))
from config.constants import DB_CREDENTIALS
from datamodel.models.userinfo import UserInfo,BillingInfo
from helpers.user_management import check_userinfo, create_new_user, user_login, user_logout


app = Flask(
    __name__,
    static_folder="../client",
    template_folder="../client",
    # static_url_path="",
)



api_url = "/api/v1/"
CORS(app)

engine = create_engine("postgresql://admin:password@localhost:5432/agile_avengers")
Session = sessionmaker(bind=engine)
session = Session()

if __name__ != "__main__":
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.INFO)
# gunicorn_logger = logging.getLogger("gunicorn.error")
# app.logger.handlers = gunicorn_logger.handlers
# app.logger.setLevel(gunicorn_logger.level)


@app.errorhandler(Exception)
def resource_not_found(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    try:
        error_object = {"error": {"status_code": code, "message": str(e).split(":", 1)[1].strip()}}
    except Exception as error:
        app.logger.info("Failed to parse the error message - {}".format(str(error)))
        error_object = e
    app.logger.info(
        "username - {}. This is the value of error object - {}".format(
            request.headers.get("X-Remote-User"), error_object
        )
    )
    return jsonify(error_object), code


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


@app.route(api_url + "/userinfo/<user_id>", methods=["GET"])
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
        return make_response(jsonify({'message': 'User not found'}),403)
    


#route to create user using input from user

@app.route(api_url + "userinfo/create_user", methods=['POST'])
def create_users():
    data = request.get_json()
    user_id = data['user_id']
    user_name = data['user_name']
    first_name = data['first_name']
    last_name = data['last_name']
    mobile_number = data['mobile_number']
    email_id = data['email_id']
    is_merchant = data['is_merchant']
    created_on = datetime.now()
    created_by = data['user_id']
    updated_on = datetime.now()
    updated_by = data['user_id']
    user = UserInfo(user_id = user_id,user_name=user_name, first_name=first_name, last_name=last_name, mobile_number=mobile_number, email_id=email_id, is_merchant=is_merchant, created_on=created_on, created_by=created_by, updated_on=updated_on, updated_by=updated_by)
    session.add(user)
    session.commit()
    return make_response(jsonify({'message': 'User created successfully'}),200)
    


# route to update user_info


@app.route(api_url + "/userinfo/update/<user_id>")
def update_user_info(user_id):
    data = request.json()
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
        return make_response(jsonify({'message': 'User not found'}),403)



# route to delete user


@app.route(api_url + "/userinfo/delete/<user_id>")
def delete_user_info(user_id):
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return jsonify({"result": True})
    else:
        return make_response(jsonify({'message': 'User not found'}),403)


#route to add debit card and billing details using input from user

@app.route(api_url + "debitcard/add", methods=['POST'])
def add_debitcard():
    data = request.get_json()
    billing_address = data['billing_address']
    postal_code = data['postal_code']
    state = data['state']
    city = data['city']
    billingaddress=BillingInfo(billing_info_id=billing_info_id,billing_address=billing_address,postal_code=postal_code,state=state,city=city)
    session.add(billingaddress)
    session.commit()
    billinginfo=session.query(BillingInfo).filter_by(billing_address=billing_address,postal_code=postal_code,state=state,city=city).first()
    card_number = data['card_number']
    user_id = data['user_id']
    card_network = data['card_network']
    cvv = data['cvv']
    billing_info_id = billinginfo['billing_info_id']
    bank_account_number = data['bank_account_number']
    created_on = datetime.now()
    created_by = data['user_id']
    updated_on = datetime.now()
    updated_by = data['user_id']
    debitcard = UserInfo(user_id = user_id,card_number=card_number, card_network=card_network, cvv=cvv, billing_info_id =billing_info_id , bank_account_number=bank_account_number, created_on=created_on, created_by=created_by, updated_on=updated_on, updated_by=updated_by)
    session.add(debitcard)
    session.commit()
    return make_response(jsonify({'message': 'User created successfully'}),200)






    



base_route = f"/api/v1/auth"


@app.route(f"{base_route}/create", methods=["POST"])
def create_user():
    user_data = request.json

    # Add to userinfo table
    ui = UserInfo(user_id=user_data["username"])
    try:
        with Session() as session:
            print("adding userinfo")
            session.add(ui)
            session.commit()
    except Exception as e:
        print(e)
        make_response(jsonify({"message": "Server Error"}), 500)

    new_user = create_new_user(user_data["username"], user_data["password"])
    print(new_user)
    if new_user is None:
        return make_response(jsonify({"message": "user already exists"}), 409)

    return jsonify({"message": "user created"})


@app.route(f"{base_route}/login", methods=["POST"])
def login():
    user_data = request.json
    token = user_login(user_data["username"], user_data["password"])
    resp = make_response(jsonify({"message": "logged in successfully"}), 200)
    for key, value in token.items():
        resp.set_cookie(key, json.dumps(value))
    resp.set_cookie("auth_token", json.dumps(token))
    return resp


@app.route(f"{base_route}/logout", methods=["POST"])
def logout():
    token = request.cookies.get("refresh_token")
    user_logout(token)
    return jsonify({"message": "logged out"})


@app.route(f"{base_route}/userinfo")
def userinfo():
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    auth_token = {"access_token": access_token, "refresh_token": refresh_token}
    token, userinfo = check_userinfo(auth_token)

    if userinfo is not None:
        resp = make_response(jsonify({"userinfo": userinfo}), 200)
        resp.set_cookie("auth_token", json.dumps(token))
        resp.set_cookie("access_token", json.dumps(token["access_token"]))
        resp.set_cookie("refresh_token", json.dumps(token["refresh_token"]))
        return resp

    return make_response(jsonify({"message": "Unauthorized"}), 403)


#   getAllPaymentMethods() {
#     const url = `${instanceUrl}/api/v1/get_all_payment_methods`;
#     return axios.get(url, config);
#   },
#   getPayeeList() {
#     const url = `${instanceUrl}/api/v1/get_payee_list`;
#     return axios.get(url, config);
#   },
#   makePayment(payload) {
#     const url = `${instanceUrl}/api/v1/make_payment`;
#     return axios.post(url, payload, config);
#   }


@app.route(api_url + "/get_all_payment_methods")
def get_all_payment_methods():
    return {
        "status": "Success",
        "data": {
            "visa - 2232": "1223",
            "Mastercard - 8881": "1234",
            "Bank Account - 1223": "9302",
            "American Express - 9282": "2323",
        },
    }


@app.route(api_url + "/get_payee_list")
def get_payee_list():
    return {"status": "Success", "data": {"aishwarya123": "123", "hemanth234": "234", "namratha345": "345"}}


@app.route(api_url + "/make_payment", methods=["POST"])
def make_payment():
    return {"status": "Success"}


@app.route(api_url + "/add_new_credit_card", methods=["POST"])
def add_new_credit_card():
    return {"status": "Success"}


@app.route(api_url + "/add_new_debit_card", methods=["POST"])
def add_new_debit_card():
    return {"status": "Success"}


if __name__ == "__main__":
    app.run(port=5000, host="localhost")
