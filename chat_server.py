# chat_server.py
import socket
import threading
import sys

def validate_port(port):
    try:
        port = int(port)
        if 1025 <= port <= 65535:
            return port
        else:
            raise ValueError
    except ValueError:
        print("Port must be an integer between 1025 and 65535.")
        sys.exit(1)

def handle_client(conn):
    print("Client connected. Type 'exit' to end chat.")
    conn.sendall(b"Welcome to the chat server! Type 'exit' to quit.\n")
    while True:
        data = conn.recv(1024).decode()
        if not data or data.strip().lower() == "exit":
            print("Client disconnected.")
            break
        print("Client:", data)
        msg = input("You: ")
        conn.sendall(msg.encode())
        if msg.strip().lower() == "exit":
            break
    conn.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python chat_server.py <port>")
        sys.exit(1)

    port = validate_port(sys.argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.listen(1)
        print(f"Server listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            handle_client(conn)

if __name__ == "__main__":
    main()

# chat_client.py
import socket
import sys
import threading

def validate_port(port):
    try:
        port = int(port)
        if 1025 <= port <= 65535:
            return port
        else:
            raise ValueError
    except ValueError:
        print("Port must be an integer between 1025 and 65535.")
        sys.exit(1)

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print("Server:", data)
        except:
            break

def main():
    if len(sys.argv) != 2:
        print("Usage: python chat_client.py <port>")
        sys.exit(1)

    port = validate_port(sys.argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(('localhost', port))
        except Exception as e:
            print(f"Connection failed: {e}")
            sys.exit(1)

        print("Connected to the server. Type 'exit' to quit.")

        # Start thread to receive messages from server
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            msg = input("You: ")
            s.sendall(msg.encode())
            if msg.strip().lower() == "exit":
                break

if __name__ == "__main__":
    main()
