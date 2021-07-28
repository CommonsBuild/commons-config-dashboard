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
from models.token_freeze_thaw import plot_token_freeze_thaw
from models.disputable_voting import (plot_dandelion_voting,
                                      plot_distribution_of_voting_phases,
                                      plot_disputable_vote_duration)
from models.augmented_bonding_curve import plot_augmented_bonding_curve

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
    return plot_token_freeze_thaw(
        opening_price=int(opening_price),
        token_freeze_period=int(token_freeze_period),
        token_thaw_period=int(token_thaw_period)
    )

@app.callback(
    Output('augmented_bonding_curve', 'figure'),
    Input('reserve_balance', 'value'),
    Input('initial_price', 'value'),
    Input('initial_supply', 'value'),
    Input('steplist', 'value')
)
#TO DO: configurable list of steps
# 3 predetermined steps, and give the user the chance to add more
# Maybe two tabs? one big buy, one big sell
def update_augmented_bonding_curve(reserve_balance,
                             initial_price,
                             initial_supply,
                             steplist):
    if None in [reserve_balance, initial_price, initial_supply]:
        raise PreventUpdate
    return plot_augmented_bonding_curve(
        reserve_balance=int(reserve_balance),
        initial_price=int(initial_price),
        initial_supply=int(initial_supply),
        steps=steplist
    )

@app.callback(
    Output('dandelion_voting', 'figure'),
    Input('support_required', 'value'),
    Input('minimum_quorum', 'value')
)
def update_dandelion_voting(support_required, minimum_quorum):
    return plot_dandelion_voting(support_required=support_required,
                          minimum_quorum=minimum_quorum)


@app.callback(
    Output('distribution_of_voting_phases', 'figure'),
    Output('disputable_voting_duration', 'figure'),
    Input('vote_duration', 'value'),
    Input('delegated_voting_period', 'value'),
    Input('quiet_ending_period', 'value'),
    Input('quiet_ending_extension', 'value'),
    Input('execution_delay', 'value')
)
def update_disputable_voting_duration(vote_duration,
                                      delegated_voting_period,
                                      quiet_ending_period,
                                      quiet_ending_extension,
                                      execution_delay):
    
    figure_distribution_of_voting_phases = plot_distribution_of_voting_phases(vote_duration=vote_duration,
                                                                              quiet_ending_period=quiet_ending_period,
                                                                              execution_delay=execution_delay,
                                                                              quiet_ending_extension=quiet_ending_extension)

    figure_disputable_vote_duration = plot_disputable_vote_duration(vote_duration=vote_duration,
                                                                         delegated_voting_period=delegated_voting_period,
                                                                         quiet_ending_period=quiet_ending_period,
                                                                         quiet_ending_extension=quiet_ending_extension,
                                                                         execution_delay=execution_delay)
    
    return figure_distribution_of_voting_phases, figure_disputable_vote_duration

if __name__ == "__main__":
    app.run_server(debug=True)
