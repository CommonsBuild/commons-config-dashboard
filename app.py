import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__,
                title="Commons Config Dash",
)

app.layout = html.Div(children=[html.H1(children='Commons Configuration Dashboard')])

if __name__ == "__main__":
    app.run_server(debug=True)
