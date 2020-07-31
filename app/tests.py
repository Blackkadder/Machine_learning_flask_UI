

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn


def data_table():
        
    data = dict(
            dates=[date(2014, 3, i+1) for i in range(10)],
            downloads=[randint(0, 100) for i in range(10)],
        )
    source = ColumnDataSource(data)

    columns = [
            TableColumn(field="dates", title="Date", formatter=DateFormatter()),
            TableColumn(field="downloads", title="Downloads"),
        ]
    data_table = DataTable(source=source, columns=columns, width=400, height=280)
    return data_table


print(data_table)