#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 19:34:18 2024

@author: elliot
"""

import nest_asyncio
import asyncio

nest_asyncio.apply()

# Now you can use asyncio.run() in environments like Jupyter or Spyder
asyncio.run(quic_client())  # or asyncio.run(run_server())
