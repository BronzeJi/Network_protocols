#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 23:33:36 2024

@author: elliot
"""

from pythonosc import udp_client

# Create an OSC client that sends to localhost on port 5005
client = udp_client.SimpleUDPClient("127.0.0.1", 12345)

# Send some messages to the server
#client.send_message("/drumbeat", 123)  # Send an integer
#client.send_message("/drumbeat", [1, 2, 3])  # Send a list of integers
client.send_message("/drumbeat", "Hello, OSC!")  # Send a string
