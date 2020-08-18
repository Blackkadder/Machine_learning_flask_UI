
import pandas as pd
from bokeh.io import output_file, show, output_notebook,curdoc
from bokeh.layouts import widgetbox, Column, row
from bokeh.embed import server_document
from bokeh.models import ColumnDataSource, Slider
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.layouts import column, grid
from bokeh.themes import Theme

def generate_app(doc):

	df = pd.read_csv('data/headcount.csv', sep = '\t')
	df = df.pivot_table(values = 'Headcount', index = ['FT or PT'],columns='Month').reset_index()
	source = ColumnDataSource(data=df)
	"""def callback(attr, old, new):
	if new == 0:
	data = df
	else:
	data = df.rolling('{0}D'.format(new)).mean()
	source.data = dict(ColumnDataSource(data=data).data)
	"""
	slider = Slider(start=0, end=30, value=0, step=2, title="Smoothing by N Days")
	#slider.on_change('value', callback)

	columns = []
	for column in df.columns:
			columns.append(TableColumn(field=column, title=column))
	data_table = DataTable(source=source, columns=columns, width=1200, height=800)
	doc.add_root(Column(slider, data_table))



def create_daterange(min_date, n_periods = 12 ):
    start_date = min_date
    n_periods = 12
    output['n_periods'] = n_periods

    date_range = pd.date_range(start =start_date,periods=n_periods+1, freq='MS')
    date_range = list(date_range.strftime('%Y-%m-%d'))
    date_range.pop(0)
    return date_range 