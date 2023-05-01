import src.config as config
import json
import requests
import traceback

def create_user(users: dict):
    user_name_id_map = {}
    for username, user_info in users.items():
        try:
            # create user
            userinfo = user_info["user_info"]
            req_body = {key: userinfo[key] for key in ["username", "password"]}
            r = requests.post(config.create_user_api, json=req_body)
            assert r.status_code == 200

            # add user-info
            req_body = dict.copy(userinfo)
            req_body["user_name"] = userinfo["username"]
            r = requests.post(config.add_userinfo_api, json=req_body)
            assert r.status_code == 200
            resp = r.json()
            user_id = resp["id"]
            user_name_id_map[username] = user_id
            
            print("Successfully created a new user")
            
            if "bank_info" in user_info:
                bank_info = user_info["bank_info"]
                bank_info["user_id"] = user_id
                r = requests.post(config.add_bank_account_api, json=bank_info)
                assert r.status_code == 200
                resp = r.json()
                print("Successfully added a bank account")
            
            if "credit_info" in user_info:
                credit_info = user_info["credit_info"]
                credit_info["user_id"] = user_id
                r = requests.post(config.add_credit_card_api, json=credit_info)
                assert r.status_code == 200
                resp = r.json()
                print("Successfully added a credit card")

        except Exception as ex:
            print(f"Failed to create user {userinfo['username']}")
            print(r.text)
            traceback.print_exc()
    
    return user_name_id_map


def make_transactions(transactions: list, user_name_id_map: dict):
    for transaction in transactions:
        try:
            transaction["payer_id"] = user_name_id_map[transaction["payer_id"]]
            transaction["payee_id"] = user_name_id_map[transaction["payee_id"]]
            r = requests.post(config.send_payment_api, json=transaction)
            assert r.status_code == 201
            print("Transaction Successful")
        except Exception as ex:
            print(f"Failed to execute the transaction")
            print(r.text)
            traceback.print_exc()


def insert_data(data: dict):
    user_name_id_map = create_user(data["users"])
    transactions = data["transactions"]
    make_transactions(transactions, user_name_id_map)