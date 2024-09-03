#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:27:51 2024

@author: elliot
"""

import asyncio
import nest_asyncio
from aioquic.asyncio.protocol import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived

async def quic_client():
    config = QuicConfiguration(is_client=True)
    config.verify_mode = False

    async with connect("localhost", 4433, configuration=config) as protocol:
        stream_id = protocol._quic.get_next_available_stream_id()
        protocol._quic.send_stream_data(stream_id, b"Hello, QUIC Server!")

        while True:
            event = await protocol._wait_for_event()
            if isinstance(event, StreamDataReceived):
                print(f"Received: {event.data.decode()}")
                break

if __name__ == "__main__":
    # Use create_task() or ensure_future() to schedule the task
    task = asyncio.create_task(quic_client())
    
nest_asyncio.apply()

# Now you can use asyncio.run() in environments like Jupyter or Spyder
asyncio.run(quic_client())  # or asyncio.run(run_server())

    # In some environments, you might not want to block the main thread
    # Optionally, you can let the event loop run and handle the task without blocking



