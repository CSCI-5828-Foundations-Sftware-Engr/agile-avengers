PORT = 5000
HOST = "0.0.0.0"
APP_NAME = "agile_avengers_data_collector"

api_version = "/v1"

## 3rd party api configs
api_hostname = "https://haveibeenpwned.com/"
all_breaches_endpoint = "api/v2/breaches"

## rabbitmq connection string
# celery_broker = "amqp://guest:guest@localhost:5672/"
celery_broker = "amqp://agile_avengers:password@rabbitmq:5672/"

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