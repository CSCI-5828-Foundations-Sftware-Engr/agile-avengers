import config
import json
import requests
import datetime
import traceback
import psycopg2


def get_data():
    try:
        url = f"{config.api_hostname}{config.all_breaches_endpoint}"
        r = requests.get(url)
        all_leaks = r.json()
        conn = psycopg2.connect(host=config.psql_host, user=config.psql_user, password=config.psql_password, dbname=config.psql_dbname)
        cursor = conn.cursor()
        for leak in all_leaks:
            add_date = int(datetime.datetime.strptime(f'{leak["BreachDate"]}', '%Y-%m-%d').timestamp())
            query = config.insert_data.replace("%s", str(add_date),1).replace("%s", json.dumps(leak),1)
            cursor.execute(query)
        conn.commit()
        return all_leaks
    except Exception as ex:
        traceback.print_exc()
    finally:
        conn.close()