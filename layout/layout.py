import dash_core_components as dcc
import dash_html_components as html

app_layout = html.Div([
    html.H1('Commons Configuration Dashboard'),
    html.Div([
        html.Div([
            html.H2('1. Token Freeze and Token Thaw'),
            html.Div([
                html.Label('Opening Price (wxDai)'),
                dcc.Input(
                    id='opening_price',
                    type='number',
                    value='2',
                    placeholder='wxDai'
                ),
            ], className='input'),
            html.Div([
                html.Label('Token Freeze Period (weeks)'),
                dcc.Input(
                    id='token_freeze_period',
                    type='number',
                    value='10',
                    placeholder='weeks'
                ),
            ], className='input'),
            html.Div([
                html.Label('Token Thaw Period (weeks)'),
                dcc.Input(
                    id='token_thaw_period',
                    type='number',
                    value='40',
                    placeholder='weeks'
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
        ], className='input-row'),
        html.Div([
            html.H2('4. Disputable Conviction Voting'),
        ], className='input-row'),
              
    ])
])