#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:01:39 2024

@author: elliot
"""

import asyncio
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, HandshakeCompleted

class EchoQuicProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            print(f"Handshake completed with {self._quic.peer_address}")
        elif isinstance(event, StreamDataReceived):
            print(f"Received data on stream {event.stream_id}: {event.data.decode()}")
            self._quic.send_stream_data(event.stream_id, event.data)
            self._quic.send_stream_data(event.stream_id, b"", end_stream=True)

async def run_server():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    await serve(
        host="localhost",
        port=4433,
        configuration=config,
        create_protocol=EchoQuicProtocol,
    )

if __name__ == "__main__":
    # Use create_task() or ensure_future() to schedule the task
    task = asyncio.create_task(run_server())

    # In some environments, you might not want to block the main thread
    # Optionally, you can let the event loop run and handle the task without blocking






