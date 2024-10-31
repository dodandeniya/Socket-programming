import socket
import argparse
import threading

# Start the client and connect to the server
def start_client(host, port, client_type, topics):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send client type and topic to the server
        client_socket.sendall(client_type.encode())  
        client_socket.recv(1024)  # Wait for server response

        topics_str = ','.join(topics)
        client_socket.sendall(topics_str.encode() if topics else b"")

        if client_type == 'pub':
            # Publisher: Allow the user to send messages
            print(f"You are connected as a publisher on topic '{topics[0] if topics else 'all'}'.")
            while True:
                message = input("Enter message to publish (or 'terminate' to quit): ")
                if message.lower() == 'terminate':
                    break
                client_socket.sendall(message.encode())
        elif client_type == 'sub':
            # Subscriber: Start a thread to receive messages from the server
            print(f"You are connected as a subscriber on topics '{', '.join(topics) if topics else 'all'}'.")
            threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
            
            # Keep the client running to receive messages until manually exited
            while True:
                if input("Type 'terminate' to quit: ").lower() == 'terminate':
                    break
        else:
            print("Invalid type. Disconnecting.")

# Function to receive messages for subscribers
def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"\n{data}")
        except ConnectionResetError:
            break

# Main function to parse arguments and start the client
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish/Subscribe TCP Client")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Server IP address')
    parser.add_argument('--port', type=int, default=6500, help='Server port')
    parser.add_argument('--type', type=str, required=True, choices=['pub', 'sub'], help='Client type: publisher or subscriber')
    parser.add_argument('--topic', type=str, help='Optional topic for publishing or subscribing')

    args = parser.parse_args()
    topics = args.topic.split(',') if args.topic else []

    start_client(args.host, args.port, args.type, topics)