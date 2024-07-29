from flask import Blueprint, request, jsonify
import socket
import threading

auth = Blueprint('auth', __name__)

messages = []

tcp_client = None

@auth.route('/notify', methods=['POST'])
def notify():
    print("A user has connected to the web page")
    return jsonify({ 'message': 'User connection logged' })

@auth.route('/send_message', methods=['POST'])
def send_message():
    global messages
    data = request.get_json()
    message = data.get('message')
    messages.append(message)
    if tcp_client:
        try:
            tcp_client.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to TCP server: {e}")
    return jsonify({'message': 'Message sent'})

@auth.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})

def receive_messages(client_socket):
    global messages
    try:
        while True:
            response = client_socket.recv(1024)
            if not response:
                break
            message = response.decode('utf-8')
            messages.append(message)
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client_socket.close()
        print("Connection to TCP server closed")

def run_client():
    global tcp_client
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000

    try:
        tcp_client.connect((server_ip, server_port))
        print("Connected to the TCP server")

        receive_thread = threading.Thread(target=receive_messages, args=(tcp_client,))
        receive_thread.start()
    except Exception as e:
        print(f"Error: {e}")

# Start the TCP client in a separate thread when the Flask app starts
threading.Thread(target=run_client, daemon=True).start()
