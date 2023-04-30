PORT = 5000
HOST = "0.0.0.0"
APP_NAME = "agile_avengers_data_collector"

api_version = "/v1"

min_balance = 1000
max_balance = 15000

## 3rd party api configs
api_hostname = "http://127.0.0.1:5000/"
create_user_api = f"{api_hostname}v1/auth/create"
add_userinfo_api = f"{api_hostname}v1/users/create"
add_credit_card = f"{api_hostname}v1/creditcard/add"
add_bank_account = f"{api_hostname}v1/bankaccount/add"

## rabbitmq connection string
celery_broker = "amqp://agile_avengers:password@localhost:5672/"
# celery_broker = "amqp://agile_avengers:password@rabbitmq:5672/"

## cron configs
daily_fetch_time = 6
default_time = 1 # years

## db configs
# local configs
# psql_host = "localhost"
# psql_user = "postgres"
# psql_password = "postgres"
# psql_dbname = "postgres"

# container configs
psql_host = "postgres"
psql_user = "admin"
psql_password = "password"
psql_dbname = "vuln_glance"

get_query = '''SELECT * from dataleaks where breach_epoch >= %s;'''
insert_data = f'''INSERT INTO dataleaks (breach_epoch, leak_info) values (%s, $$%s$$);'''
## create table command 
# create table dataleaks (leak_id serial primary key, breach_epoch integer not null, leak_info jsonb not null);