import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import plotly.express as px
import pandas as pd

server = flask.Flask(__name__) # define flask app.server


app = dash.Dash(__name__,
                title="Commons Config Dash",
                suppress_callback_exceptions=True,
                )

app.layout = html.Div(children=[html.H1(children='Commons Configuration Dashboard')])

if __name__ == '__main__':
    app.run_server(debug=True)
