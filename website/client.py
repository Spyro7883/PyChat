import socket
import threading

def receive_messages(client_socket):
    try:
        while True:
            response = client_socket.recv(1024)
            if not response:
                break
            print(f"\nReceived: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client_socket.close()
        print("Connection to server closed")

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    server_port = 8000

    try:
        client.connect((server_ip, server_port))
        print("Connected to the server")

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        while True:
            msg = input()
            if msg.lower() == "close":
                client.send(msg.encode("utf-8"))
                break
            client.send(msg.encode("utf-8")[:1024])

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")

if __name__ == '__main__':
    run_client()
