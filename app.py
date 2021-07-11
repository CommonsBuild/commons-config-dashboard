# General Dependencies
import plotly.express as px
import pandas as pd

# Dash dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from layout.layout import app_layout
from models.token_freeze_thaw import token_freeze_thaw

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                title="Commons Config Dash",
                external_stylesheets=external_stylesheets
)

app.layout = app_layout
server = app.server

# Callbacks
@app.callback(
    Output('token_freeze_thaw', 'figure'),
    Input('opening_price', 'value'),
    Input('token_freeze_period', 'value'),
    Input('token_thaw_period', 'value')
)
def update_token_freeze_thaw(opening_price,
                             token_freeze_period,
                             token_thaw_period):
    if None in [opening_price, token_freeze_period, token_thaw_period]:
        raise PreventUpdate
    return token_freeze_thaw(
        opening_price=int(opening_price),
        token_freeze_period=int(token_freeze_period),
        token_thaw_period=int(token_thaw_period)
    )

if __name__ == "__main__":
    app.run_server(debug=True)
