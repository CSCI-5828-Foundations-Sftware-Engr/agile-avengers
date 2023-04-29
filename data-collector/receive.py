import pika
import os
import sys
import json

def main():
    credentials = pika.PlainCredentials(username='agile_avengers', password='password')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='transaction')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body))
        resp = json.loads(body)
        print(f"username is {resp['username']}, name is {resp['name']}")

    channel.basic_consume(queue='transaction',
                        auto_ack=True,
                        on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)