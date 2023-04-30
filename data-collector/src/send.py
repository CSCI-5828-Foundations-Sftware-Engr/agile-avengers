import pika
import json
from src.generator import generate_user_info, generate_bank_info, generate_credit_card

user = {'username': 'taylor30', 'name': 'Hunter Harper', 'sex': 'M', 'address': '184 Richard Square Apt. 319\nPort Colin, UT 10026', 'mail': 'hunterdawn@hotmail.com'}

def send_data():
    credentials = pika.PlainCredentials(username='agile_avengers', password='password')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='transaction')
    
    data = [
        {
            "user_info": generate_user_info(),
            "bank_info": generate_bank_info(),
            "credit_info": generate_credit_card()
        }
    ]
    channel.basic_publish(exchange='',
                        routing_key='transaction',
                        body=json.dumps(data))

    connection.close()
