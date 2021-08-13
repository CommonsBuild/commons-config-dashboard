import dash_core_components as dcc
import dash_html_components as html

app_layout = html.Div(
    [
        html.H1("Commons Configuration Dashboard"),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("1. Token Freeze and Token Thaw"),
                        html.Div(
                            [
                                html.Label("Opening Price (wxDai)"),
                                dcc.Slider(
                                    id="opening_price",
                                    value=2,
                                    min=1,
                                    max=5,
                                    step=0.5,
                                    updatemode="drag",
                                    tooltip={"always_visible": False},
                                    marks={
                                        1: "1",
                                        2: "2",
                                        3: "3",
                                        4: "4",
                                        5: "5",
                                    },
                                ),
                            ],
                            className="input",
                        ),
                        html.Div(
                            [
                                html.Label("Token Freeze Period (weeks)"),
                                dcc.Slider(
                                    id="token_freeze_period",
                                    value=10,
                                    min=2,
                                    max=20,
                                    step=1,
                                    updatemode="drag",
                                    tooltip={"always_visible": False},
                                    marks={
                                        2: "2",
                                        10: "10",
                                        20: "20",
                                    },
                                ),
                            ],
                            className="input",
                        ),
                        html.Div(
                            [
                                html.Label("Token Thaw Period (weeks)"),
                                dcc.Slider(
                                    id="token_thaw_period",
                                    value=20,
                                    min=10,
                                    max=30,
                                    step=1,
                                    updatemode="drag",
                                    tooltip={"always_visible": False},
                                    marks={10: "5", 20: "20", 30: "30"},
                                ),
                            ],
                            className="input",
                        ),
                    ],
                    className="input-row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="token_freeze_thaw"),
                            ],
                            className="output",
                        )
                    ],
                    className="output-row",
                ),
                html.Div(
                    [
                        html.H2("2. The Augmented Bonding Curve (ABC)"),
                        html.Div(
                            [
                                html.Label(
                                    "Choose initial Funding  collected in the hatch"
                                ),
                                dcc.Dropdown(
                                    id="hatch_funding",
                                    options=[
                                        {"label": "400k", "value": "400"},
                                        {"label": "1M", "value": "1000"},
                                        {"label": "2M", "value": "2000"},
                                    ],
                                    value="1000",
                                ),
                            ],
                            className="input",
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Percentage of Funds to go to the commons pool"
                                ),
                                dcc.Slider(
                                    id="commons_percentage",
                                    value=25,
                                    min=0,
                                    max=95,
                                    step=1,
                                    updatemode="drag",
                                    tooltip={"always_visible": False},
                                    marks={
                                        0: "0%",
                                        25: "25%",
                                        50: "50%",
                                        75: "75%",
                                        95: "95%",
                                    },
                                ),
                            ],
                            className="input",
                        ),
                    ],
                    className="input-row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Initial Price (wxDai)"),
                                dcc.Slider(
                                    id="initial_price",
                                    value=1.5,
                                    min=1,
                                    max=4,
                                    step=0.01,
                                    updatemode="drag",
                                    tooltip={"always_visible": False},
                                    marks={1: "1", 2: "2", 3: "3", 4: "4"},
                                ),
                            ],
                            className="input",
                        ),
                        html.Div(
                            [
                                html.Label("Entry Tribute (%)"),
                                dcc.Slider(
                                    id="entry_tribute",
                                    value=5,
                                    min=0,
                                    max=99,
                                    step=1,
                                    updatemode="drag",
                                    tooltip={"always_visible": False},
                                    marks={
                                        0: "0%",
                                        25: "25%",
                                        50: "50%",
                                        75: "75%",
                                        99: "99%",
                                    },
                                ),
                            ],
                            className="input",
                        ),
                        html.Div(
                            [
                                html.Label("Exit Tribute (%)"),
                                dcc.Slider(
                                    id="exit_tribute",
                                    value=5,
                                    min=0,
                                    max=99,
                                    step=1,
                                    updatemode="drag",
                                    tooltip={"always_visible": False},
                                    marks={
                                        0: "0%",
                                        25: "25%",
                                        50: "50%",
                                        75: "75%",
                                        99: "99%",
                                    },
                                ),
                            ],
                            className="input",
                        ),
                    ],
                    className="input-row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Scenario"),
                                dcc.Dropdown(
                                    id="steplist",
                                    options=[
                                        {"label": "Big Buy", "value": "1"},
                                        {"label": "Big Sell", "value": "2"},
                                    ],
                                    value="1",
                                ),
                            ],
                            className="input",
                        ),
                    ],
                    className="input-row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Zoom in?"),
                                dcc.Dropdown(
                                    id="zoom_graph",
                                    options=[
                                        {"label": "No", "value": "0"},
                                        {"label": "Yes", "value": "1"},
                                    ],
                                    value="0",
                                ),
                            ],
                            className="input",
                        ),
                    ],
                    className="input-row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="augmented_bonding_curve"),
                            ],
                            className="output",
                        )
                    ],
                    className="output-row",
                ),
                html.Div(
                    [
                        html.Div(id="buy_sell_table")
                    ],
                    className="output-row",
                ),
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
            html.Div([
                html.Label('Relative Spending Limit (%)'),
                dcc.Slider(
                    id='relative_spending_limit',
                    value=10,
                    min=0,
                    max=10,
                    step=1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        0 : '0%',
                        5 : '5%',
                        10 : '10%',
                    }
                ),
            ], className='input'),
            html.Div([
                html.Label('Conviction Growth (%)'),
                dcc.Slider(
                    id='conviction_growth',
                    value=2,
                    min=0,
                    max=20,
                    step=0.5,
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
                html.Label('Minimum Conviction (%)'),
                dcc.Slider(
                    id='minimum_conviction',
                    value=2,
                    min=0,
                    max=5,
                    step=0.1,
                    updatemode='drag',
                    tooltip={'always_visible' : False},
                    marks={
                        0 : '0%',
                        2.5 : '2.5%',
                        5 : '5%',
                    }
                ),
            ], className='input'),
        ], className='input-row'),
        html.Div([
            html.Div([
                dcc.Graph(id='graph_conviction_decay'),
            ], className='output'),
            html.Div([
                dcc.Graph(id='graph_effective_supply_approve'),
            ], className='output'),
            html.Div([
                dcc.Graph(id='graph_disputable_conviction_voting'),
                dcc.RadioItems(
                    options=[
                        {'label': '7 Days', 'value': 7},
                        {'label': '2 Weeks', 'value': 14},
                        {'label': '1 Month', 'value': 30},
                        {'label': '3 Months', 'value': 90},
                        {'label': '6 Months', 'value': 180}
                    ],
                    value='MTL',
                    labelStyle={'display': 'inline-block'}
                )  
            ], className='output'),  
        ], className='output-row'),
              
    ])
])