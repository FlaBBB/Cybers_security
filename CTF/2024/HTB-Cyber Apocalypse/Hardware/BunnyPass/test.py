import json

import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters("94.237.50.175", 57167))
channel = connection.channel()

QUEUE_NAME = "my_queue"

# Declare a queue
channel.queue_declare(queue=QUEUE_NAME)

# Define callback function to handle incoming messages
datas = []


def callback(ch, method, properties, body):
    print("Received message:", body)
    datas.append(body)


# Start consuming messages
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit, press CTRL+C")
# Keep consuming messages until the user interrupts with CTRL+C
channel.start_consuming()

with open(f"{QUEUE_NAME}-out.txt", "w") as f:
    f.write(json.dumps(datas))
