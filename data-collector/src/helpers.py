import src.config as config
import json
import requests
import traceback

# def get_data():
#     try:
#         url = f"{config.api_hostname}{config.all_breaches_endpoint}"
#         r = requests.get(url)
#         all_leaks = r.json()
#         conn = psycopg2.connect(host=config.psql_host, user=config.psql_user, password=config.psql_password, dbname=config.psql_dbname)
#         cursor = conn.cursor()
#         for leak in all_leaks:
#             add_date = int(datetime.datetime.strptime(f'{leak["BreachDate"]}', '%Y-%m-%d').timestamp())
#             query = config.insert_data.replace("%s", str(add_date),1).replace("%s", json.dumps(leak),1)
#             cursor.execute(query)
#         conn.commit()
#         return all_leaks
#     except Exception as ex:
#         traceback.print_exc()
#     finally:
#         conn.close()

def create_user(data):
    for entry in data:
        try:
            # create user
            userinfo = entry["user_info"]
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
            
            print("Successfully created a new user")
            
            if "bank_info" in entry:
                bank_info = entry["bank_info"]
                bank_info["user_id"] = user_id
                r = requests.post(config.add_bank_account, json=bank_info)
                assert r.status_code == 200
                resp = r.json()
                print("Successfully added a bank account")
            
            if "credit_info" in entry:
                credit_info = entry["credit_info"]
                credit_info["user_id"] = user_id
                r = requests.post(config.add_credit_card, json=credit_info)
                assert r.status_code == 200
                resp = r.json()
                print("Successfully added a credit card")

        except Exception as ex:
            print(f"Failed to create user {userinfo['username']}")
            print(r.text)
            traceback.print_exc()