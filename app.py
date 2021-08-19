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
from models.disputable_conviction_voting import (plot_coviction_voting_decay,
                                                 plot_disputable_conviction_voting,
                                                 plot_percent_effective_supply_approve_proposal_time_chart)
from models.disputable_voting import (plot_dandelion_voting,
                                      plot_distribution_of_voting_phases,
                                      plot_disputable_vote_duration)
from models.augmented_bonding_curve import (BondingCurveHandler) 





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
        opening_price=float(opening_price),
        token_freeze_period=float(token_freeze_period),
        token_thaw_period=float(token_thaw_period)
    )

@app.callback(
    Output('augmented_bonding_curve', 'figure'),
    Output('buy_sell_table', 'children'),
    Input('commons_percentage', 'value'),
    Input('ragequit_percentage', 'value'),
    Input('initial_price', 'value'),
    Input('entry_tribute', 'value'),
    Input('exit_tribute', 'value'),
    Input('hatch_scenario_funding', 'value'),
    Input('steplist', 'value'),
    Input('zoom_graph', 'value')
) 
def update_augmented_bonding_curve(
                             commons_percentage,
                             ragequit_percentage,
                             initial_price,
                             entry_tribute,
                             exit_tribute,
                             hatch_scenario_funding,
                             steplist,
                             zoom_graph,
                             ):

    if commons_percentage >= 100 or commons_percentage < 0:
        raise PreventUpdate
    if None in [commons_percentage, ragequit_percentage, initial_price, entry_tribute, exit_tribute, zoom_graph]:
        raise PreventUpdate

    if(steplist=="1"):
        steplist = [[5, "TEC"], [1000, "wxDai"], [10, "TEC"]]
    elif(steplist=="2"):
        steplist = [[30, "wxDai"], [25, "TEC"], [30, "wxDai"]]

    bCurve_handler = BondingCurveHandler(
                             commons_percentage,
                             ragequit_percentage,
                             initial_price,
                             entry_tribute,
                             exit_tribute,
                             hatch_scenario_funding,
                             steplist,
                             zoom_graph)

    return bCurve_handler.get_data()

@app.callback(
    Output('dandelion_voting', 'figure'),
    Input('support_required', 'value'),
    Input('minimum_quorum', 'value')
)
def update_dandelion_voting(support_required, minimum_quorum):
    return plot_dandelion_voting(support_required=support_required,
                          minimum_quorum=minimum_quorum)

@app.callback(
    Output('graph_conviction_decay', 'figure'),
    Output('graph_effective_supply_approve', 'figure'),
    Output('graph_disputable_conviction_voting', 'figure'),
    Input('relative_spending_limit', 'value'),
    Input('conviction_growth', 'value'),
    Input('minimum_conviction', 'value')
)
def update_disputable_conviction_voting(relative_spending_limit,
                                        conviction_growth,
                                        minimum_conviction):
    figure_conviction_decay = plot_coviction_voting_decay(relative_spending_limit=relative_spending_limit,
                                             conviction_growth=conviction_growth,
                                             minimum_conviction=minimum_conviction)

    figure_disputable_conviction_voting = plot_disputable_conviction_voting(relative_spending_limit=relative_spending_limit,
                                             conviction_growth=conviction_growth,
                                             minimum_conviction=minimum_conviction)
                                            
    figure_percent_effective_supply = plot_percent_effective_supply_approve_proposal_time_chart(relative_spending_limit=relative_spending_limit,
                                             conviction_growth=conviction_growth,
                                             minimum_conviction=minimum_conviction)
    
    return (figure_conviction_decay, figure_percent_effective_supply, figure_disputable_conviction_voting)

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
