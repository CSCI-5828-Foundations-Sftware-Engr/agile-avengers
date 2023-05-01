import json
import traceback

import requests

import src.config as config
from src.celery import celery_app
from src.helpers import create_user
from src.send import send_data

# @celery_app.task()
# def fetch_new_leaks():
#     try:
#         url = f"{config.api_hostname}{config.all_breaches_endpoint}"
#         r = requests.get(url)
#         all_leaks = r.json()
#         new_window = int((datetime.datetime.utcnow() - relativedelta(hours=config.daily_fetch_time)).timestamp())
#         # new_window = int((datetime.datetime.utcnow() - relativedelta(years=25)).timestamp())
#         conn = psycopg2.connect(host=config.psql_host, user=config.psql_user, password=config.psql_password, dbname=config.psql_dbname)
#         cursor = conn.cursor()
#         for leak in all_leaks:
#             add_date = int(datetime.datetime.strptime(f'{leak["BreachDate"]}', '%Y-%m-%d').timestamp())
#             if add_date >= new_window:
#                 print("Got a new leak to insert")
#                 query = config.insert_data.replace("%s", str(add_date),1).replace("%s", json.dumps(leak),1)
#                 cursor.execute(query)
#         conn.commit()
#     except Exception as ex:
#         traceback.print_exc()
#     finally:
#         conn.close()


@celery_app.task()
def generate_data():
    send_data()


# @celery_app.task()
# def store_entry(data):
#     create_user(data)
