import socket

# Define the server address and port
HOST = '127.0.0.1'  # The server's IP address (change as needed)
PORT = 65432        # The same port as used by the server

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))  # Connect to the server
    print(f"Connected to server at {HOST}:{PORT}")
    
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
