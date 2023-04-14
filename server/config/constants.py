import os

DB_HOSTNAME = os.environ.get("DB_HOSTNAME", "localhost")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

DB_CREDENTIALS = {
    "HOSTNAME": DB_HOSTNAME,
    "DB_NAME": "agile_avengers",
    "USERNAME": "admin",
    "PASSWORD": DB_PASSWORD,
    "SSLCERT": "",
    "SSLKEY": "",
    "SSLROOTCERT": "",
}