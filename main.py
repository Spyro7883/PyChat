from website import create_app
import threading
from website.server import run_server

app = create_app()

# Start the TCP server in a separate thread
tcp_server_thread = threading.Thread(target=run_server, daemon=True)
tcp_server_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
