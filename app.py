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
                external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[html.H1(children='Commons Configuration Dashboard')])

if __name__ == '__main__':
    app.run_server(debug=True)