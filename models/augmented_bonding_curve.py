import os
import pandas as pd
import param as pm
import panel as pn
import plotly.express as px
import plotly.graph_objects as go
import hvplot.pandas
import holoviews as hv
import numpy as np

class BondingCurveInitializer:

    def __init__(self, initial_supply=200, initial_price=5, initial_balance=200):
        self.initial_supply = initial_supply
        self.initial_price = initial_price
        self.initial_balance = initial_balance
    
    def reserve_ratio(self):
        return self.initial_balance / (self.initial_price * self.initial_supply)
    
    def x(self):
        return np.linspace(0, 1000, 1000)
    
    def price(self, supply):
        return (supply**((1/self.reserve_ratio())-1) * self.initial_price) / (self.initial_supply**((1/self.reserve_ratio())-1))
    
    def curve(self, x):
        y = self.price(x)
        return pd.DataFrame(zip(x,y),columns=['supply (in thousands)','price'])
    
    def initial_point(self):
        points = hv.Points((self.initial_supply,self.initial_price))
        return points.opts(color='k', size=10)
    
    def outputs(self):
        return "Reserve Ratio: {0:.2f}".format(self.reserve_ratio())
    
    def view(self):
        hv.extension('bokeh')
        curve = self.curve(self.x())
        return curve.hvplot.line(x='supply (in thousands)', y='price', line_width=8) * self.initial_point()

class BondingCurve(BondingCurveInitializer):
    current_supply = pm.Number(500, bounds=(1,1000), step=1)
    
    def current_balance(self):
        return self.reserve_ratio() * self.price(self.current_supply) * self.current_supply
    
    def current_point(self):
        points = hv.Points((self.current_supply,self.price(self.current_supply)))
        return points.opts(color='red', size=10)

    def outputs(self):
        return "Initial price: {0:.2f}\n\rCurrent price: {1:.2f}".format(self.initial_price, self.price(self.current_supply))

    def view(self):
        hv.extension('bokeh')
        curve = self.curve(self.x())
        return curve.hvplot.line(x='supply (in thousands)', y='price', line_width=8) * self.initial_point() * self.current_point()

class BondingCurveCalculator(BondingCurve):
    amount = pm.Number(0, bounds=(-10000, 10000))
    
    def sell(self, bonded):
        return self.current_balance() * ((bonded / self.current_supply + 1)** (1/self.reserve_ratio()) - 1)
    
    def buy(self, collateral):
        return self.current_supply * ((collateral / self.current_balance() + 1)** (self.reserve_ratio()) - 1)
    
    def new_supply(self):
        return max(0, min(self.current_supply + self.buy(self.amount), 1000))

    def new_point(self):
        new_supply = self.new_supply()
        points = hv.Points((new_supply, self.price(new_supply)))
        return points.opts(color='green', size=10)
    
    def outputs(self):
        return "Current price: {0:.2f}\n\rNew price: {1:.2f}".format(self.price(self.current_supply), self.price(self.new_supply()))

    def view(self):
        hv.extension('bokeh')
        curve = self.curve(self.x())
        return curve.hvplot.line(x='supply (in thousands)', y='price', line_width=8) * self.current_point() * self.new_point()

def plot_augmented_bonding_curve(reserve_balance=200, initial_price=10, initial_supply=200, steps=[]):
    res = BondingCurveInitializer(reserve_balance, initial_price, initial_supply)
    curve = res.curve(res.x())
    fig = px.line(curve, x='reserve_balance', y='price')
    print(steps)
    actual_balance = reserve_balance
    return fig
    #draw steps (vertical lines for now)
    #   draw initial line
"""     fig.add_vline(
        x=actual_balance,
        line_width=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="Initial State",  
        annotation_position="top"
        )
    #  for each step in array of steps (received as argument)
    for i, step in enumerate(steps):
        actual_balance += int(step)
        fig.add_vline(
        x=actual_balance,
        line_width=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="Step " + str(i+1),  
        annotation_position="top"
        ) """



""" OLD VERSION, DELETE ONCE ABOVE WORKS WELL
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import hvplot.pandas

class ReserveRatio:
    def __init__(self, reserve_balance=300000, initial_price=5, reserve_ratio=0.2):
        self.reserve_ratio = reserve_ratio
        self.price = initial_price
        self.reserve_balance = reserve_balance
    
    def x(self):
        return np.linspace(0, self.reserve_balance*4, 1000)
    
    def curve(self, x):
        #print(self.reserve_ratio)
        #print(self.reserve_balance)
        y = (x**((1/self.reserve_ratio)-1) * self.price) / (self.reserve_balance**((1/self.reserve_ratio)-1))
        return pd.DataFrame(zip(x,y),columns=['reserve_balance','price'])
    
    def view(self):
        curve = self.curve(self.x())
        return curve.hvplot.line(x='reserve_balance',y='price', line_width=8)




def plot_augmented_bonding_curve(reserve_balance=20000, initial_price=10, reserve_ratio=20, steps=[]):
    res = ReserveRatio(reserve_balance, initial_price, reserve_ratio/100)
    curve = res.curve(res.x())
    fig = px.line(curve, x='reserve_balance', y='price')
    #print(steps)
    actual_balance = reserve_balance
    #draw steps (vertical lines for now)
    #   draw initial line
    fig.add_vline(
        x=actual_balance,
        line_width=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="Initial State",  
        annotation_position="top"
        )
    #  for each step in array of steps (received as argument)
    for i, step in enumerate(steps):
        actual_balance += int(step)
        fig.add_vline(
        x=actual_balance,
        line_width=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="Step " + str(i+1),  
        annotation_position="top"
        )
    
    return fig


"""