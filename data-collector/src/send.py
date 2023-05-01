import pika
import json
import os 
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
from src.generator import generate_fake_data

user = {'username': 'taylor30', 'name': 'Hunter Harper', 'sex': 'M', 'address': '184 Richard Square Apt. 319\nPort Colin, UT 10026', 'mail': 'hunterdawn@hotmail.com'}

def send_data():
    credentials = pika.PlainCredentials(username='agile_avengers', password='password')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='transaction')
    
    
    channel.basic_publish(exchange='',
                        routing_key='transaction',
                        body=json.dumps(generate_fake_data()))
    print("Queued data for insertion")

    connection.close()

send_data()