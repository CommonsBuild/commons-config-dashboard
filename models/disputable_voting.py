import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_dandelion_voting(support_required=10, minimum_quorum=50):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 100], y=[0, 100], fill='tozeroy',
                        mode='none'
    ))
    fig.add_trace(go.Scatter(x=[0, 100], y=[0, support_required], fill='tozeroy',
                        mode='none'
    ))
    fig.add_trace(go.Scatter(x=[0, minimum_quorum], y=[0, minimum_quorum], fill='tozeroy',
                        mode='none'
    ))
    
    return fig


def plot_distribution_of_voting_phases(vote_duration=3,
                                  quiet_ending_period=1,
                                  execution_delay=1,
                                  quiet_ending_extension=2):
    
    non_quiet_voting_period = vote_duration - quiet_ending_period

    labels = ['Non-Quiet Voting Period','Quiet Voting Period','Execution Delay','Quiet Ending Extension']
    values = [non_quiet_voting_period, quiet_ending_period, execution_delay, quiet_ending_extension]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    return fig


def plot_disputable_vote_duration(vote_duration=1,
                                  delegated_voting_period=1,
                                  quiet_ending_period=1,
                                  quiet_ending_extension=1,
                                  execution_delay=1):
    

    fig = go.Figure()
    
    # Voting Process
    fig.add_trace(go.Bar(
        y=['Voting Process'],
        x=[vote_duration - quiet_ending_period],
        name='Non-Quiet Voting Period',
        orientation='h',
        marker=dict(
            color='orange',
        )
    ))
    fig.add_trace(go.Bar(
        y=['Voting Process'],
        x=[quiet_ending_period],
        name='Quiet Ending Period',
        orientation='h',
        marker=dict(
            color='yellow',
        )
    ))
    fig.add_trace(go.Bar(
        y=['Voting Process'],
        x=[execution_delay],
        name='Execution Delay',
        orientation='h',
        marker=dict(
            color='light blue',
        ),
    ))
    fig.add_trace(go.Bar(
        y=['Delegated Voting Period'],
        x=[delegated_voting_period],
        name='Delegated Voting Period',
        orientation='h',
        marker=dict(
            color='red',
        )
    ))
    
    # Voting Process With an Extension
    fig.add_trace(go.Bar(
        y=['Voting Process With an Extension'],
        x=[vote_duration],
        name='Delegated & Non-Delegated Voting',
        orientation='h',
        marker=dict(
            color='green',
        )
    ))
    
    fig.add_trace(go.Bar(
        y=['Voting Process With an Extension'],
        x=[quiet_ending_period],
        name='Quiet Ending Extension',
        orientation='h',
        marker=dict(
            color='green',
        )
    ))
    
    fig.add_trace(go.Bar(
        y=['Voting Process With an Extension'],
        x=[quiet_ending_extension],
        name='Quiet Ending Extension',
        orientation='h',
        marker=dict(
            color='purple',
        )
    ))
    
    fig.add_trace(go.Bar(
        y=['Voting Process With an Extension'],
        x=[execution_delay],
        name='Execution Delay',
        orientation='h',
        marker=dict(
            color='blue',
        )
    ))
    
    fig.add_vline(
        x=vote_duration,
        line_width=1.5,
        line_color="gray",
        annotation_text='Vote Duration', 
        annotation_position="top"
    )

    fig.update_layout(
        xaxis_title='Days',
        barmode='stack',
        xaxis = dict(
            dtick=1    
        )
    )

    return fig