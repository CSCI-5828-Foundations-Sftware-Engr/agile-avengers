import json
import os
import sys

import pika

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
from src.helpers import insert_data
import src.config as config


def callback(ch, method, properties, body):
    print(" [x] Received %r" % json.loads(body))
    data = json.loads(body)
    insert_data(data)
    # print(f"username is {resp['username']}, name is {resp['name']}")


def main():
    credentials = pika.PlainCredentials(username=config.rabbitmq_user, password=config.rabbitmq_password)
    parameters = pika.ConnectionParameters(
        host=config.rabbitmq_host, port=config.rabbitmq_port, virtual_host="/", credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="transaction")

    channel.basic_consume(
        queue="transaction", auto_ack=True, on_message_callback=callback
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
