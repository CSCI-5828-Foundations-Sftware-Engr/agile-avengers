import os

DB_USERNAME = "admin"
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_HOSTNAME = os.environ.get("DB_HOSTNAME", "localhost")
DB_NAME = "agile_avengers"
