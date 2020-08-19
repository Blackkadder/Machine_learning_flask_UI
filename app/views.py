# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm


from datetime import date
from random import randint
from bokeh.layouts import widgetbox
from bokeh.embed import server_document
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.embed import components
from datetime import date
from random import randint
from bokeh.plotting import figure
import yaml
import pandas as pd
import GOSWB as go


# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # cut the page for authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))
            
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template( 'pages/register.html', form=form, msg=msg )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template( 'pages/register.html', form=form, msg=msg )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # cut the page for authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template( 'pages/login.html', form=form, msg=msg )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    """
    This is the index page

    """

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None
    headcount_df = go.get_df()
    
    headcount_df =  headcount_df.pivot_table(values= 'HEADCOUNT',index = [ 'FULL_OR_PART_TIME'],
                        columns = 'Date', aggfunc='sum'
                ).reset_index()
    table_headcount = headcount_df.to_html(classes ='table table-head-bg-primary mt-4')
    table_hours = headcount_df.to_html(classes ='table table-head-bg-primary mt-4')
    table_rates = headcount_df.to_html(classes ='table table-head-bg-primary mt-4')
    table_wages = headcount_df.to_html(classes ='table table-head-bg-primary mt-4')
    table_adjustments = headcount_df.to_html(classes ='table table-head-bg-primary mt-4')


        # try to match the pages defined in -> pages/<input file>
    return render_template( 'pages/'+path , table_headcount = table_headcount,
                                            table_hours = table_hours,
                                            table_rates = table_rates,
                                            table_wages = table_wages,
                                            table_adjustments = table_adjustments )
    
    #except:
        
    #    return render_template( 'pages/error-404.html' )

@app.route('/new_prediction.html')
def new_prediction():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    

        # try to match the pages defined in -> pages/<input file>
    return render_template( 'pages/'+'new_prediction.html' ,  )
    

# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')


#@app.route('/', methods=['GET'])
#def bkapp_page():
#    script = server_document('http://localhost:5006/bkapp')
#    return render_template("pages/index.html", script=script, template="Flask", relative_urls=False)


@app.route('/get_table', methods=['GET','POST'])
def get_table():

    # extract nrow, ncol via ajax post - contained in request.form
    start_date = request.form.get('start_date', type=str)
    
    # the updated/new plot
    #p = figure(plot_width=150, plot_height=100)

    #p.line(list(range(nrow)), list(range(nrow)))

    df = go.get_df()
    df = df[df['FT or PT'] =='FT']

    #table_script, table_div = data_table(df)
    #plot_script, plot_div = bar_chart(df)
    doc_script = df.to_html(classes ='table table-head-bg-primary mt-4')

 

        # try to match the pages defined in -> pages/<input file>
    return render_template( 'pages/get_table.html' ,  doc_script = doc_script )



def data_table(df):
    
    data = dict(df)
    source = ColumnDataSource(data)

    columns = [
            TableColumn(field="Month", title="Month"),
            TableColumn(field="FT or PT", title="FT or PT"),
            TableColumn(field="Headcount", title="Headcount"),
        
        ]
    data_table = DataTable(source=source, columns=columns, width=800, height=600,   editable=True,)
    return components(data_table)


def bar_chart(df):
    # prepare some data
    df = df.groupby(['Month']).sum().reset_index()

    month = list(df['Month'].values)
    headcount = list(df['Headcount'].values)

    # output to static HTML file

    # create a new plot with a title and axis labels
    source = ColumnDataSource(data=dict(df))
    p2 = figure(title="simple line example", x_range=month,)#)x_axis_label='month', y_axis_label='headcount')
    p2.sizing_mode = 'stretch_width'

    # add a line renderer with legend and line thickness
    p2.vbar(x = 'Month', top = 'Headcount', width =  0.5, legend_label="Temp.", line_width=2, color = 'blue',source = source)
    #p2.line(x, y, legend_label="Temp.", line_width=2,color = 'blue' )
    #p2.line(x, y, legend_label="Temp.", line_width=2,color = 'orange')


    # show the results
    return components(p2)



