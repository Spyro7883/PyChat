from website import create_app
import threading
from website.server import run_server
from website.auth import run_client

app = create_app()

# Start the TCP server in a separate thread
tcp_server_thread = threading.Thread(target=run_server, daemon=True)
tcp_server_thread.start()

# Start the TCP client in a separate thread
tcp_client_thread = threading.Thread(target=run_client, daemon=True)
tcp_client_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
