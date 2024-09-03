#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 13:04:32 2024

@author: elliot
"""

import socket

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "Hello, UDP Server!"
    client_socket.sendto(message.encode(), ('localhost', 12345))

    response, _ = client_socket.recvfrom(1024)
    print(f"Received from server: {response.decode()}")

    client_socket.close()

if __name__ == "__main__":
    udp_client()
