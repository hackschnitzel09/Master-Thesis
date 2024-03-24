from http.server import BaseHTTPRequestHandler, HTTPServer
import pika
from urllib.parse import urlparse, parse_qs
import threading


host = '0.0.0.0'
port = 8080

user="guest"
password="guest"
amqphost="rabbitmq"
amqpport=5672

connection = pika.BlockingConnection(pika.ConnectionParameters(amqphost, amqpport, credentials=pika.PlainCredentials(user, password)))

channel = connection.channel()

def send_msg(method, msg):
    channel.queue_declare(queue=method)
    out_que = method
    channel.basic_publish(exchange='',
                        routing_key=out_que,
                        body= msg)
    print(" [x] Sent " + msg + " to " + out_que)


class RequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        print('Options request received')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, DELETE, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        

    def do_GET(self):
        print('GET request received')

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write("GET request received\n".encode('utf-8'))
        
        parsed_url=urlparse(self.path)
        print(parsed_url)
        if parsed_url.path == '/tasks':
            send_msg("get", "all")
        elif parsed_url.path.startswith('/tasks/'):
            task_id = parsed_url.path.split('/')[2]
            send_msg("get", task_id)
        else:
            print('Invalid request path:', parsed_url.path)
            self.send_error(404)  # Sendet einen 404-Fehler zurück


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
       # print('POST request received')
        send_msg("post", post_data.decode('utf-8'))

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write("POST request received\n".encode('utf-8'))
   

    def do_DELETE(self):
        parsed_url=urlparse(self.path)
        if parsed_url.path.startswith('/tasks/'):
            task_id = parsed_url.path.split('/')[2]
        print('Task ID to delete:', task_id)
        send_msg("delete", task_id)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write("DELETE request received\n".encode('utf-8'))

server = HTTPServer((host, port), RequestHandler)

print('Server running on {}:{}'.format(host, port))
server.serve_forever()