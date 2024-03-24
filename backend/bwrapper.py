import json
import pika
import requests

backend="http://backend:5011/tasks"

user="guest"
password="guest"
host="rabbitmq"
port=5672


def send_msg(queue, msg):
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='',
                        routing_key=queue,
                        body= msg)
    print(" [x] Sent " + msg + " to " + queue)


def get(ch, method, properties, body):
    queue="return"
    if body.decode() == "all":
        response = requests.get(backend)
        json_data = response.json()
        send_msg(queue, json.dumps(json_data))
        #print(response)


def post(ch, method, properties, body):
    response = requests.post(backend, json=json.loads(body), verify=False)
    if response.status_code == 201:
       print('POST request was successful!')
       print('Response:', response.json())  # Die Antwort des Servers als JSON ausgeben
    else:
       print('Error:', response.status_code)


def delete(ch, method, properties, body):
    global backend
    task_id = body.decode()  # Annahme: Die Task-ID ist im Body der Nachricht enthalten
    backend = backend + "/" + format(task_id)  # Die URL für den DELETE-Request erstellen
    response = requests.delete(backend, verify=False)  # DELETE-Request an das Flask-Backend senden
    if response.status_code == 200:
        print('DELETE request was successful!')
        print('Response:', response.json())  # Die Antwort des Servers als JSON ausgeben
    else:
        print('Error:', response.status_code)




connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, credentials=pika.PlainCredentials(user, password)))
channel = connection.channel()
channel.queue_declare(queue="post")
channel.basic_consume(queue="post", on_message_callback=post, auto_ack=True)
channel.queue_declare(queue="delete")
channel.basic_consume(queue="delete", on_message_callback=delete, auto_ack=True)
channel.queue_declare(queue="get")
channel.basic_consume(queue="get", on_message_callback=get, auto_ack=True)
channel.start_consuming()