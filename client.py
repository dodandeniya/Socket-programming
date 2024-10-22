"""
To run: python client.py --host 127.0.0.1 --port 5000
"""

import socket
import argparse

# # Define the server address and port
# HOST = '127.0.0.1'  # The server's IP address (change as needed)
# PORT = 6500        # The same port as used by the server

# Set up argument parsing
parser = argparse.ArgumentParser(description="TCP Client")
parser.add_argument('--host', type=str, default='127.0.0.1', help='Server IP address')
parser.add_argument('--port', type=int, default=6500, help='Server port')

args = parser.parse_args()

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((args.host, args.port))  # Connect to the server
    print(f"Connected to server at {args.host}:{args.port}")
    
    # Keep sending and receiving data
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        
        # Send data
        client_socket.sendall(message.encode())
        
        # Receive the response from the server
        data = client_socket.recv(1024)  # Buffer size of 1024 bytes
        print(f"Received from server: {data.decode()}")

