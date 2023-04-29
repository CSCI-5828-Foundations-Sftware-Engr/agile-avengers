import pika
import json

credentials = pika.PlainCredentials(username='agile_avengers', password='password')
parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='transaction')

user = {'username': 'taylor30', 'name': 'Hunter Harper', 'sex': 'M', 'address': '184 Richard Square Apt. 319\nPort Colin, UT 10026', 'mail': 'hunterdawn@hotmail.com'}
channel.basic_publish(exchange='',
                      routing_key='transaction',
                      body=json.dumps(user))
print(" [x] Sent user info")

connection.close()
