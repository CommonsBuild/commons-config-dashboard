import pandas as pd
import plotly.express as px

def token_freeze_thaw(opening_price=100, token_freeze_period=10, token_thaw_period=30):
    weekly_token_thaw = opening_price/token_thaw_period
    df = pd.DataFrame({ 'week' : range(1,61)})
    df['price'] = 0
    df.loc[df['week'] <= token_freeze_period, 'price'] = opening_price
    df.loc[df['week'] > token_freeze_period, 'price'] = opening_price - (df['week'] - token_freeze_period) * weekly_token_thaw
    df.loc[df['price'] < 0, 'price'] = 0
    
    fig = px.line(df, x='week', y='price')
    
    fig.add_vline(
        x=token_freeze_period,
        line_width=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="End of Token Freeze", 
        annotation_position="top"
    )

    fig.add_vline(
        x=token_thaw_period + token_freeze_period,
        line_width=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="End of Token Thaw", 
        annotation_position="top"
    )

    return fig