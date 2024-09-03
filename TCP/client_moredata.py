#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:43:32 2024

@author: elliot
"""

import socket  # Import the socket module

def tcp_client():
    """
    This function creates a TCP client that can send multiple messages to a server
    and receive responses from the server.
    """
    
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the server address and port to connect to
    server_address = ('localhost', 12345)
    
    # Connect the socket to the server's address and port
    client_socket.connect(server_address)
    
    try:
        # List of messages to send
        messages = ["Hello, Server!", "How are you?", "Goodbye!"]
        
        for message in messages:
            # Send each message to the server
            client_socket.send(message.encode())
            print(f"Sent: {message}")
            
            # Receive a response from the server
            response = client_socket.recv(1024)
            print(f"Received: {response.decode()}")
    
    finally:
        # Close the connection to the server
        client_socket.close()
        print("Connection closed.")

# Run the TCP client if this script is executed directly
if __name__ == "__main__":
    tcp_client()
