"""
To run: python server.py --host 127.0.0.1 --port 5000
"""

import socket
import argparse

# # Define the server address and port
# HOST = '127.0.0.1'  # localhost (change to actual IP if running on a different machine)
# PORT = 6500        # Arbitrary non-privileged port

# Set up argument parsing
parser = argparse.ArgumentParser(description="TCP Server")
parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind the server')
parser.add_argument('--port', type=int, default=6500, help='Port to bind the server')

args = parser.parse_args()

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((args.host, args.port))  # Bind the socket to the address
    server_socket.listen()  # Listen for incoming connections
    print(f"Server listening on {args.host}:{args.port}")
    
    # Accept a connection
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            # Receive data from the client
            data = conn.recv(1024)  # Buffer size of 1024 bytes
            if not data:
                break  # Exit loop if no data is received
            print(f"Received: {data.decode()}")

            # Send a response back to the client
            conn.sendall(data)

