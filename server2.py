import socket
import threading
import argparse

# List to store all connected subscribers
subscribers = []

# Handle client connections
def handle_client(conn, addr):
    print(f"Client connected: {addr}")

    # Ask if the client is a publisher or subscriber
    conn.sendall(b"Are you a publisher or subscriber? (pub/sub): ")
    client_type = conn.recv(1024).decode().strip().lower()

    if client_type == 'pub':
        conn.sendall(b"You are connected as a publisher.\n")
        handle_publisher(conn)
    elif client_type == 'sub':
        conn.sendall(b"You are connected as a subscriber.\n")
        subscribers.append(conn)
        handle_subscriber(conn)
    else:
        conn.sendall(b"Invalid choice. Closing connection.\n")
        conn.close()

# Function to handle publisher clients
def handle_publisher(conn):
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(f"Publisher sent: {message}")
            broadcast(message)  # Send message to all subscribers
        except ConnectionResetError:
            break

    print("Publisher disconnected")
    conn.close()

# Function to handle subscriber clients
def handle_subscriber(conn):
    while True:
        try:
            data = conn.recv(1024)  # Keep the connection open to receive broadcasts
            if not data:
                break
        except ConnectionResetError:
            break

    print("Subscriber disconnected")
    conn.close()
    subscribers.remove(conn)

# Broadcast message to all subscribers
def broadcast(message):
    for subscriber in subscribers:
        try:
            subscriber.sendall(f"Message from publisher: {message}".encode())
        except Exception as e:
            print(f"Error sending to subscriber: {e}")
            subscribers.remove(subscriber)
    

# Main function to parse arguments and start the server
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish/Subscribe TCP Server")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind the server')
    parser.add_argument('--port', type=int, default=6500, help='Port to bind the server')

    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((args.host, args.port))
        server_socket.listen()
        print(f"Server listening on {args.host}:{args.port}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()