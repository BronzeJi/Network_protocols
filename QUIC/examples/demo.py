#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 19:27:22 2024

@author: elliot
"""

#
# demo application for http3_server.py
#

import datetime
import os
from urllib.parse import urlencode

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocketDisconnect

import numpy as np
import simpleaudio as sa

ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.environ.get("STATIC_ROOT", os.path.join(ROOT, "htdocs"))# Defines the root directory for static files (e.g., images, CSS, JavaScript), defaulting to htdocs unless overridden by an environment variable
STATIC_URL = "/"
LOGS_PATH = os.path.join(STATIC_ROOT, "logs")#The directory where logs are stored.
QVIS_URL = "https://qvis.quictools.info/"

templates = Jinja2Templates(directory=os.path.join(ROOT, "templates"))# Jinja2 as the templating engine for rendering HTML templates


async def homepage(request):
    """
    Simple homepage.
    """
    await request.send_push_promise("/style.css")
    return templates.TemplateResponse("index.html", {"request": request})


async def echo(request):
    """
    HTTP echo endpoint.
    """
    content = await request.body()
    media_type = request.headers.get("content-type")
    return Response(content, media_type=media_type)


async def logs(request):
    """
    Browsable list of QLOG files.
    """
    logs = []
    for name in os.listdir(LOGS_PATH):
        if name.endswith(".qlog"):
            s = os.stat(os.path.join(LOGS_PATH, name))
            file_url = "https://" + request.headers["host"] + "/logs/" + name
            logs.append(
                {
                    "date": datetime.datetime.utcfromtimestamp(s.st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "file_url": file_url,
                    "name": name[:-5],
                    "qvis_url": QVIS_URL
                    + "?"
                    + urlencode({"file": file_url})
                    + "#/sequence",
                    "size": s.st_size,
                }
            )
    return templates.TemplateResponse(
        "logs.html",
        {
            "logs": sorted(logs, key=lambda x: x["date"], reverse=True),
            "request": request,
        },
    )


# async def padding(request):
#     """
#     Dynamically generated data, maximum 50MB.
#     """
#     size = min(50000000, request.path_params["size"])
#     return PlainTextResponse("Z" * size)

def generate_tone(frequency, duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Generate sine wave
    audio = wave * (2**15 - 1) / np.max(np.abs(wave))  # Normalize to 16-bit range
    return audio.astype(np.int16)  # Convert to 16-bit data


def play_tone(frequency ,duration=1.0):
    tone=generate_tone(frequency, duration)
    play_obj=sa.play_buffer(tone ,1, 2, 44100)
    play_obj.wait_done()


async def padding(request):
    number_to_note_freq={
        1: 262, #C4
        2: 294, #D
        3: 329, #E
        4: 349, #F
        5: 392, #G
        6: 440, #A
        7: 493, #B
        }
    size = request.path_params["size"] 
    # Find the corresponding frequency or return a default message
    frequency = number_to_note_freq.get(size)
    if frequency:
        #Play the tone at the corresponding frequency
        play_tone(frequency)
        return PlainTextResponse(f"Play sound with f {frequency} Hz")
    else:
        return PlainTextResponse("Number out of range. Please enter a number bewteen 1 and 7. ")

async def ws(websocket):
    """
    WebSocket echo endpoint.
    """
    if "chat" in websocket.scope["subprotocols"]:
        subprotocol = "chat"
    else:
        subprotocol = None
    await websocket.accept(subprotocol=subprotocol)

    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(message)
    except WebSocketDisconnect:
        pass


async def wt(scope: Scope, receive: Receive, send: Send) -> None:
    """
    WebTransport echo endpoint.
    """
    # accept connection
    message = await receive()
    assert message["type"] == "webtransport.connect"
    await send({"type": "webtransport.accept"})

    # echo back received data
    while True:
        message = await receive()
        if message["type"] == "webtransport.datagram.receive":
            await send(
                {
                    "data": message["data"],
                    "type": "webtransport.datagram.send",
                }
            )
        elif message["type"] == "webtransport.stream.receive":
            await send(
                {
                    "data": message["data"],
                    "stream": message["stream"],
                    "type": "webtransport.stream.send",
                }
            )


starlette = Starlette(
    routes=[
        Route("/", homepage),
        Route("/{size:int}", padding),
        Route("/echo", echo, methods=["POST"]),
        Route("/logs", logs),
        WebSocketRoute("/ws", ws),
        Mount(STATIC_URL, StaticFiles(directory=STATIC_ROOT, html=True)),
    ]
)


async def app(scope: Scope, receive: Receive, send: Send) -> None:
    if scope["type"] == "webtransport" and scope["path"] == "/wt":
        await wt(scope, receive, send)
    else:
        await starlette(scope, receive, send)