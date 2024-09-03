#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:11:04 2024

@author: elliot
"""

import socket

def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port (localhost and port 12345)
    server_socket.bind(('localhost', 12345))
    
    # Listen for incoming connections (max 1 connection in the queue)
    server_socket.listen(1)
    print("TCP Server is listening on port 12345...")

    # Accept a connection from a client
    conn, addr = server_socket.accept() # Client Port
    print(f"Connected by {addr}")
    
    # Receive data from the client (up to 1024 bytes)
    data = conn.recv(1024).decode()
    print(f"Received from client: {data}")

    # Send back
    response = "Hello, TCP Client!"
    conn.send(response.encode()) # Encode the string to bytes and send it through the connection

    conn.close()

if __name__ == "__main__":
    tcp_server()
