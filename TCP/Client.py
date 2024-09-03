#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:12:23 2024

@author: elliot
"""

import socket  # Import the socket module to create and manage TCP sockets

def tcp_client():
    # Create a TCP/IP socket (AF_INET is for IPv4, SOCK_STREAM is for TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the server address and port to connect to
    server_address = ('localhost', 12345)

    try:
        # Connect the socket to the server's address and port
        client_socket.connect(server_address)
        print(f"Connected to server at {server_address}")

        
        # Send the message to the server
        message = "Hello, TCP Server!"
        client_socket.send(message.encode()) # encode the string into bytes
        print(f"Sent: {message}")

        # Receive a response from the server
        # The buffer size is set to 1024 bytes, which is the maximum amount of data to receive at once
        response = client_socket.recv(1024)
        
        # Decode the received bytes back into a string
        print(f"Received: {response.decode()}")

    except ConnectionError as e:
        # Handle any connection errors (e.g., server not available, connection refused)
        print(f"Connection error: {e}")

    finally:
        # Close the socket connection after communication is done
        client_socket.close()
        print("Connection closed.")

# If this script is run directly, execute the tcp_client function while import cannt.
if __name__ == "__main__":
    tcp_client()
