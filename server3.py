"""
To run: python server3.py --host 127.0.0.1 --port 3000
"""

import socket
import threading
import argparse
from collections import defaultdict

# Dictionary to store subscribers based on the topic
subscribers = defaultdict(list)


def handle_client(connection, address):
    print(f"Client connected: {address}")

    # Ask if the client is a publisher or subscriber
    connection.sendall(b"Are you a publisher or subscriber? (pub/sub): ")
    client_type = connection.recv(1024).decode().strip().lower()

    # Ask for the topics
    connection.sendall(
        b"Enter the topic(s), separated by commas (or leave blank for all): ")
    topics = connection.recv(1024).decode().strip().split(',')

    topics = [topic.strip() for topic in topics if topic.strip()]

    if client_type == 'pub':
        connection.sendall(b"You are connected as a publisher.\n")
        # Publishers still publish to one topic
        handle_publisher(conn, topics[0] if topics else None)
    elif client_type == 'sub':
        connection.sendall(b"You are connected as a subscriber.\n")

        if topics:
            for topic in topics:
                subscribers[topic].append(connection)
        else:
            subscribers["all"].append(connection)
        handle_subscriber(connection, topics)
    else:
        connection.sendall(b"Invalid choice. Closing connection.\n")
        connection.close()

# Function to handle publisher clients


def handle_publisher(connection, topic):
    while True:
        try:
            message = connection.recv(1024).decode()
            if not message:
                break
            print(f"Publisher sent on topic '{topic or 'all'}': {message}")
            # Send message to all subscribers of the topic
            broadcast(message, topic)
        except ConnectionResetError:
            break

    print("Publisher disconnected")
    connection.close()


# Function to handle subscriber clients
def handle_subscriber(conn, topics):
    while True:
        try:
            # Keep the connection open to receive broadcasts
            data = conn.recv(1024)
            if not data:
                break
        except ConnectionResetError:
            break

    print("Subscriber disconnected")
    conn.close()
    for topic in topics:
        if conn in subscribers[topic]:
            subscribers[topic].remove(conn)

# Broadcast message to all subscribers of a specific topic


def broadcast(message, topic):
    targate_subscribers = subscribers[topic] if topic else subscribers["all"]
    for subscriber in targate_subscribers:
        try:
            subscriber.sendall(f"Message on topic '{
                               topic or 'all'}': {message}".encode())
        except Exception as e:
            print(f"Error sending to subscriber: {e}")
            subscribers[topic].remove(subscriber)


# Main function to parse arguments and start the server
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Publish/Subscribe TCP Server")
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host to bind the server')
    parser.add_argument('--port', type=int, default=6500,
                        help='Port to bind the server')

    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((args.host, args.port))
        server_socket.listen()
        print(f"Server listening on {args.host}:{args.port}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(conn, addr))
            client_thread.start()
