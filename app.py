import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.express as px
import pandas as pd

server = flask.Flask(__name__) # define flask app.server

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                server=server,
                title="Commons Config Dash",
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[html.H1(children='Commons Configuration Dashboard')])
