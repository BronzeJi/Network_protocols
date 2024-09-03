#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 23:31:57 2024

@author: elliot
"""

from pythonosc import dispatcher
from pythonosc import osc_server

def print_handler(address, *args):
    print(f"Received OSC message at {address} with arguments: {args}")

# Define the dispatcher to map addresses to handler functions
disp = dispatcher.Dispatcher()
disp.map("/drumbeat", print_handler)  # The address "/drumbeat" maps to the print_handler

# Create the OSC server
server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 12345), disp)
print("Serving on {}".format(server.server_address))

# Start the server, it will run forever
server.serve_forever()
