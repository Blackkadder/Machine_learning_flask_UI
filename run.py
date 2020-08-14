# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from threading import Thread

from app import app, db
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.io import output_file, show, output_notebook,curdoc
from bokeh.layouts import widgetbox
from bokeh.embed import server_document
from bokeh.models import ColumnDataSource, Slider
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import components
from datetime import date
from random import randint
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.layouts import column, grid
from bokeh.themes import Theme
#from socket import *


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': generate_app}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()


def generate_app(doc):

	import pandas as pd 

	df = pd.read_csv("example.csv", index_col=0)
	data_source = ColumnDataSource(df)
	line_plot1 = figure(sizing_mode="stretch_both")
	line_plot1.line(
	    source=data_source,
	    x="x",
	    y="y",
	)
	line_plot2 = figure(sizing_mode="stretch_both")
	line_plot2.line(
	    source=data_source,
	    x="y",
	    y="x",
	)
	sliders = [
	    Slider(start=0, end=5, value=5, step=1, title="Max X"),
	    Slider(start=0, end=25, value=25, step=1, title="Max Y"),
	]

	def update_graph(attr, old, new):
	    x_max = sliders[0].value
	    y_max = sliders[1].value
	    filtered_df = df[(df["x"] <= x_max) & (df["y"] <= y_max)]
	    new_data = ColumnDataSource(filtered_df).data
	    data_source.data = dict(new_data)

	for slider in sliders:
	    slider.on_change("value", update_graph)

	layout = grid(
	    [
	        [
	            line_plot1,
	            column(sliders),
	        ],
	        line_plot2,
	    ],
	    sizing_mode="stretch_both",
	)

	doc.add_root(layout)
    


if __name__ == "__main__":
    Thread(target=bk_worker).start()
   
    app.run(port = 8000)
