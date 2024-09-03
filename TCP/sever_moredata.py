#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:43:00 2024

@author: elliot
"""

import socket  # Import the socket module

def tcp_server():
    """
    This function creates a TCP server that can handle multiple messages from clients.
    It receives messages, prints them, and sends a response back to the client.
    """
    
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the server address and port
    server_address = ('localhost', 12345)
    
    # Bind the socket to the address and port
    server_socket.bind(server_address)
    
    # Start listening for incoming connections
    server_socket.listen(1)
    print(f"Server is listening on {server_address}")
    
    while True:
        # Accept a connection from a client
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        
        try:
            while True:
                # Receive data from the client (up to 1024 bytes)
                data = conn.recv(1024)
                
                # Check if the connection is closed by the client
                if not data:
                    print("Client disconnected")
                    break
                
                # Print the received data
                print(f"Received: {data.decode()}")
                
                # Define a response message
                response = "Message received!"
                
                # Send the response back to the client
                conn.send(response.encode())
        
        finally:
            # Close the connection to the client
            conn.close()
            print("Connection closed.")

# Run the TCP server if this script is executed directly
if __name__ == "__main__":
    tcp_server()
