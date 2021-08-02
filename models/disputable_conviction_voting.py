import plotly.express as px
import plotly.graph_objects as go

import os
os.environ['HV_DOC_HTML'] = 'true'
import pandas as pd
import param as pm
import panel as pn
import hvplot.pandas
import holoviews as hv
import numpy as np

pn.extension()

class SimplifiedConvictionVoting(pm.Parameterized):
    halflife = pm.Number(2, bounds=(0, 20), step=0.5)
    max_ratio = pm.Number(0.1, bounds=(0,1), step=0.01)
    min_threshold = pm.Number(0.025, bounds=(0,0.2), step=0.005)
    min_active_stake_pct = 0.05
    
    staked_on_proposal = 1
    staked_on_other_proposals = 0
    requested = pm.Number(0.01, bounds=(0, 0.1), step=0.001)
    
    def decay(self):
        return (1 / 2) ** (1 / self.halflife)
    
    def weight(self):
        return self.min_threshold * self.max_ratio ** 2

    def conviction(self, initial_conviction, amount, time):
        return initial_conviction * self.decay() ** time + (amount * (1 - self.decay() ** time)) / (1 - self.decay())

    def staked_on_proposals(self):
        return self.staked_on_proposal + self.staked_on_other_proposals
    
    def staked(self, staked = None):
        if staked is None:
            staked = self.staked_on_proposals()
        return np.where(staked > self.min_active_stake_pct, staked, self.min_active_stake_pct) # np.max([staked, self.min_active_stake_pct])

    def max_conviction(self, amount):
        return amount / (1 - self.decay())

    def threshold(self, requested_pct):
        return self.weight() / (self.max_ratio - requested_pct) ** 2 if np.any(requested_pct <= self.max_ratio) else float('inf')
    
    def min_conviction_to_pass(self, initial_conviction, time):
        min_conviction_to_pass = (self.min_threshold - (initial_conviction * self.decay() ** time)) * (1 - self.decay())/(1 - self.decay()** time)
        return min_conviction_to_pass

    def view_conviction_time_chart(self):
        x = np.linspace(0,20,1000)
        y = 100 * self.conviction(0, self.staked_on_proposal, time=x) / self.max_conviction(self.staked())
        threshold = self.threshold(self.requested) 
        y2 = 100 * np.linspace(threshold, threshold, 1000)
        df = pd.DataFrame(zip(x, y, y2), columns=['time (days)','conviction (%)', 'threshold (%)'])
        return df.hvplot.line(x='time (days)',y='conviction (%)', color="purple") * df.hvplot.line(x='time (days)',y='threshold (%)',color="red")
    
    def view_conviction_growth_decay_time_chart(self):
        x = np.linspace(0, 5 * self.halflife,1000)
        y = 100 * self.conviction(0, self.staked_on_proposal, time=x) / self.max_conviction(self.staked())
        threshold = self.threshold(self.requested) 
        df_growth = pd.DataFrame(zip(x, y), columns=['time (days)','conviction (%)'])
        
        x2 = np.linspace(5 * self.halflife,10 * self.halflife,1000)
        y2 = y[-1] * self.decay()**x
        df_decay = pd.DataFrame(zip(x2, y2), columns=['time (days)','conviction (%)'])
        
        df = pd.concat([df_growth, df_decay])
        #return df.hvplot.line(x='time (days)',y='conviction (%)', color="purple")
        return df
    
    def view_percent_effective_supply_approve_proposal_time_chart(self):
        x = np.linspace(0,8,1000)
        y = 100 * self.min_conviction_to_pass(0, time=x) / self.conviction(0, 1, time=x)
        #x = np.linspace(0, 100, 1000)
        #y = 100 * self.staked_on_proposal / self.staked(np.where(x / 100 >= self.staked_on_proposal, x/100, np.max([self.staked_on_proposal, self.min_active_stake_pct])))
        df = pd.DataFrame(zip(x,y), columns=['time (days)','Effective Supply (%)'])
        #return df.hvplot.line(x='time (days)', y='Effective Supply (%)', color="purple")
        return df
    
    
    def view_threshold_chart(self):
        x = np.linspace(0, 100 * (self.max_ratio - np.sqrt(self.weight())), 1000)
        y = 100 * self.threshold(x / 100)
        df = pd.DataFrame(zip(x,y), columns=['requested (%)', 'threshold (%)'])
        #return df.hvplot.line(x='requested (%)', y='threshold (%)', color='red') * hv.VLine(100 * self.requested)
        return df


def plot_coviction_voting_decay(relative_spending_limit=20,
                                 conviction_growth=10,
                                 minimum_conviction=15):
    scv = SimplifiedConvictionVoting()
    scv.halflife = conviction_growth
    df_decay_cv = scv.view_conviction_growth_decay_time_chart()
    fig = px.line(df_decay_cv, x='time (days)', y='conviction (%)')
    fig.update_yaxes(title='Voting Power (%)')
    fig.update_xaxes(range=[0,100])
    return fig


def plot_percent_effective_supply_approve_proposal_time_chart(relative_spending_limit=20,
                                 conviction_growth=10,
                                 minimum_conviction=15):
    scv = SimplifiedConvictionVoting()
    scv.halflife = conviction_growth
    scv.min_threshold = minimum_conviction/100
    scv.requested = 0.01
    df_percent_effective_supply = scv.view_percent_effective_supply_approve_proposal_time_chart()
    fig = px.line(df_percent_effective_supply, x='time (days)', y='Effective Supply (%)')
    fig.update_yaxes(range=[0,2])
    return fig


def plot_disputable_conviction_voting(relative_spending_limit=20,
                                 conviction_growth=10,
                                 minimum_conviction=15):
    scv = SimplifiedConvictionVoting()
    df_simplified_cv = scv.view_threshold_chart()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df_simplified_cv['requested (%)'], y=df_simplified_cv['threshold (%)'], name="placeholder")
    )
    fig.add_vline(x=relative_spending_limit,
                  name="test",
                  line_dash="dot",
                  line_color="pink",
                  annotation_text="Relative Spending Limit")
    fig.add_trace(
            go.Scatter(
                mode="markers+text",
                x=[0],
                y=[minimum_conviction],
                marker_symbol=["line-ew"],
                text="Minimum % of tokens needed to pass",
                textposition="top center",
                marker_line_width=2,
                showlegend=False,
            )
    )
    
    return fig