import socket
import threading

clients = []

def handle_client(client_socket, addr):
    global clients
    try:
        clients.append(client_socket)
        broadcast(f"{addr} has joined the chat.", client_socket)
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request or request.lower() == "close":
                break
            print(f"Received from {addr}: {request}")
            broadcast(request, client_socket)
    except Exception as e:
        print(f"Error when handling client {addr}: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")
        broadcast(f"{addr} has left the chat.", client_socket)

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error broadcasting message: {e}")

def run_server():
    server_ip = "127.0.0.1"
    port = 8000

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

if __name__ == '__main__':
    run_server()
