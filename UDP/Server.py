#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:54:51 2024

@author: elliot
"""

import socket

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    server_socket.bind(('localhost', 12345))
    print("UDP Server is listening on port 12345...")

    # Receive data from the client
    data, addr = server_socket.recvfrom(1024)
    print(f"Received from client: {data.decode()}")

    # Send the response back to the client
    response = "Hello, UDP Client!"
    server_socket.sendto(response.encode(), addr)

if __name__ == "__main__":
    udp_server()
