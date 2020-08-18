# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from threading import Thread

from app import app, db
from bokeh.server.server import Server
from tornado.ioloop import IOLoop

from datetime import date
from random import randint
import GOSWB as go

#from socket import *


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': go.generate_app}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()


if __name__ == "__main__":
    Thread(target=bk_worker).start()
   
    app.run(port = 8000)
