import socket
import sys

def start_client(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', port))

            welcome = client_socket.recv(1024).decode()
            print(welcome.strip())

            while True:
                message = input("You: ")
                client_socket.sendall(message.encode())

                if message.lower() == "exit":
                    print("Disconnected from server.")
                    break

                data = client_socket.recv(1024)
                reply = data.decode().strip()
                print(f"Server: {reply}")

                if reply.lower() == "exit":
                    print("Server ended the chat.")
                    break
    except ConnectionRefusedError:
        print("Connection failed. Ensure the server is running and port is correct.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chat_client.py <port>")
        sys.exit(1)

    try:
        port_num = int(sys.argv[1])
        start_client(port_num)
    except ValueError:
        print("Port must be an integer.")
