import dash_core_components as dcc
import dash_html_components as html

app_layout = html.Div([
    html.H1('Commons Configuration Dashboard'),
    html.Div([
        html.Div([
            html.H2('1. Token Freeze and Token Thaw'),
            html.Div([
                html.Label('Opening Price (wxDai)'),
                dcc.Slider(
                    id='opening_price',
                    value=2,
                    min=1,
                    max=5,
                    step=0.5,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        1 : '1',
                        2 : '2',
                        3 : '3',
                        4 : '4',
                        5 : '5',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Token Freeze Period (weeks)'),
                dcc.Slider(
                    id='token_freeze_period',
                    value=10,
                    min=2,
                    max=20,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        2 : '2',
                        10 : '10',
                        20 : '20',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Token Thaw Period (weeks)'),
                dcc.Slider(
                    id='token_thaw_period',
                    value=20,
                    min=10,
                    max=30,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        10 : '5',
                        20 : '20',
                        30 : '30'
                    }
                ),
            ], className='input'),
        ], className='input-row'),
        html.Div([
            html.Div([
                dcc.Graph(id='token_freeze_thaw'),
            ], className='output')
        ], className='output-row'),
        html.Div([
            html.H2('2. The Augmented Bonding Curve (ABC)'),
        ], className='input-row'),
        html.Div([
            html.H2('3. Disputable Voting'),
            html.Div([
                html.Label('Support Required (%)'),
                dcc.Slider(
                    id='support_required',
                    value=20,
                    min=0,
                    max=100,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        0 : '0%',
                        50 : '50%',
                        100 : '100%',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Minimum Quorum (%)'),
                dcc.Slider(
                    id='minimum_quorum',
                    value=20,
                    min=0,
                    max=100,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        0 : '0%',
                        50 : '50%',
                        100 : '100%',
                    }
                ),
            ], className='input'),
        ], className='input-row'),
        html.Div([
            html.Div([
                dcc.Graph(id='dandelion_voting'),
            ], className='output')
        ], className='output-row'),
            html.Div([
            html.Div([
                html.Label('Vote Duration (days)'),
                dcc.Slider(
                    id='vote_duration',
                    value=5,
                    min=1,
                    max=10,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        1: '1 day',
                        5 : '5 days',
                        10 : '10 days',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Delegated Voting Period (days)'),
                dcc.Slider(
                    id='delegated_voting_period',
                    value=5,
                    min=1,
                    max=10,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        1: '1 day',
                        5 : '5 days',
                        10 : '10 days',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Quiet Ending Period (days)'),
                dcc.Slider(
                    id='quiet_ending_period',
                    value=5,
                    min=1,
                    max=10,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        1: '1 day',
                        5 : '5 days',
                        10 : '10 days',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Quiet Ending Extension (days)'),
                dcc.Slider(
                    id='quiet_ending_extension',
                    value=5,
                    min=1,
                    max=10,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        1: '1 day',
                        5 : '5 days',
                        10 : '10 days',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Execution Delay (days)'),
                dcc.Slider(
                    id='execution_delay',
                    value=5,
                    min=1,
                    max=10,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        1: '1 day',
                        5 : '5 days',
                        10 : '10 days',
                    }
                ),
            ], className='input'),
        ], className='input-row-large'),
        html.Div([
            html.Div([
                dcc.Graph(id='distribution_of_voting_phases'),
            ], className='output')
        ], className='output-row'),
        html.Div([
            html.Div([
                dcc.Graph(id='disputable_voting_duration'),
            ], className='output')
        ], className='output-row'),
        html.Div([
            html.H2('4. Disputable Conviction Voting'),
        ], className='input-row'),
              
    ])
])