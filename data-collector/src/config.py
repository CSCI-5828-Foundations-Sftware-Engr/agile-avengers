PORT = 5000
HOST = "0.0.0.0"
APP_NAME = "agile_avengers_data_collector"

api_version = "/v1"

min_balance = 1000
max_balance = 15000

num_users = 5
num_merchants = 5
num_transactions = 20

api_hostname = "http://backend-svc:5000/"
# api_hostname = "http://127.0.0.1:5000/"  # un-comment when running locally
create_user_api = f"{api_hostname}v1/auth/create"
add_userinfo_api = f"{api_hostname}v1/users/create"
add_credit_card_api = f"{api_hostname}v1/creditcard/add"
add_bank_account_api = f"{api_hostname}v1/bankaccount/add"
send_payment_api = f"{api_hostname}v1/payment/send"

## rabbitmq connection string
rabbitmq_user = "agile_avengers"
rabbitmq_password = "password"
rabbitmq_host = "rabbitmq"
# rabbitmq_host = "localhost" # un-comment when running locally
rabbitmq_port = "5672" 
# celery_broker = "amqp://agile_avengers:password@rabbitmq:5672/"
celery_broker = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/"

## cron configs
daily_fetch_time = 6
