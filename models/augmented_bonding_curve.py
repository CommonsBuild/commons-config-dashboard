import os
import pandas as pd
import param as pm
import panel as pn
from param.parameterized import output
import plotly.express as px
import plotly.graph_objects as go
import hvplot.pandas
import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash
import numpy as np


class BondingCurveInitializer:
    def __init__(self, reserve_balance=100, initial_price=5, initial_supply=100):
        self.initial_price = initial_price
        self.initial_supply = initial_supply
        self.initial_balance = reserve_balance

    def reserve_ratio(self):
        return self.initial_balance / (self.initial_price * self.initial_supply)

    def x(self):
        return np.linspace(0, self.initial_supply*4, 1000)

    #Returns the token price given a specific supply
    def price(self, supply):
        return (supply ** ((1 / self.reserve_ratio()) - 1) * self.initial_price) / (
            self.initial_supply ** ((1 / self.reserve_ratio()) - 1)
        )

    #For drawing the bonding curve
    def curve(self, x):
        y = self.price(x)
        return pd.DataFrame(zip(x, y), columns=["supply (in thousands)", "price"])




class BondingCurve(BondingCurveInitializer):
    def __init__(self, reserve_balance=100, initial_price=5, initial_supply=100, entry_tribute=0.05, exit_tribute=0.05):
        super().__init__(reserve_balance, initial_price, initial_supply)
        self.current_supply = self.initial_supply
        self.entry_tribute = entry_tribute
        self.exit_tribute = exit_tribute

    def current_balance(self):
        return (
            self.reserve_ratio() * self.price(self.current_supply) * self.current_supply
        )

    #Returns how much wxDai you get from selling TEC
    def sell(self, bonded):
        return self.current_balance() * (
            (bonded / self.current_supply + 1) ** (1 / self.reserve_ratio()) - 1
        )

    #Returns how much TEC you get from purchasing with wxDai
    def buy(self, collateral):
        return self.current_supply * (
            (collateral / self.current_balance() + 1) ** (self.reserve_ratio()) - 1
        )


def generate_outputs_table(bondingCurve, steplist):

    column_names = [
        "Current Price",
        "Current Supply",
        "Amount in",
        "Tribute collected",
        "Amount out",
        "New Price",
        "New Supply",
        "Slippage",
    ]
    outputTable = pd.DataFrame(columns=column_names)

    for step in steplist:

        current_price = bondingCurve.price(bondingCurve.current_supply)

        # check if tribute gets applied before or after!!!!
        amount_in = step[0]
        amount_in_parsed = str(amount_in) + " " + str(step[1])
      
        amount_out = 0
        amount_out_parsed = ""
        new_supply = 0
        tribute_collected = 0
        if step[1] == "wxDai":
            # take tribute and buy
            tribute_collected = amount_in * bondingCurve.entry_tribute
            amountAfterTribute = amount_in - tribute_collected

            amount_out = bondingCurve.buy(amountAfterTribute)
            amount_out_parsed = str(amount_out) + " TEC"
            tribute_collected_parsed = str(tribute_collected) + " wxDai"

            slippage = (amount_in - tribute_collected)/bondingCurve.price(bondingCurve.current_supply) - amount_out
            slippage_pct = slippage / ((amount_in - tribute_collected)/bondingCurve.price(bondingCurve.current_supply))

            new_supply = max(
                0, min(bondingCurve.current_supply + amount_out, 1000)
            )
        elif step[1] == "TEC":
            #this section is a bit of a mess with -1 mults. Surely there is a better way, revisit
            # sell and take tribute
            amount_in = amount_in * -1 #because we are reducing the supply (burning)
            amountBeforeTribute = bondingCurve.sell(amount_in)            

            tribute_collected = amountBeforeTribute * bondingCurve.exit_tribute #since it is a sale, the number returned is negative
            tribute_collected_parsed = str(tribute_collected*-1) + " wxDai"
            amount_out = (amountBeforeTribute - tribute_collected) #we leave it negative for the supply calculation below
            amount_out_parsed = str(amount_out*-1) + " wxDai" 


            #print( (amount_in*(1-bondingCurve.exit_tribute)))
            #print(bondingCurve.price(bondingCurve.current_supply))
            #print(amount_out)
            slippage = ((amount_in*(1-bondingCurve.exit_tribute))*bondingCurve.price(bondingCurve.current_supply) - amount_out) *-1
            slippage_pct = slippage / ((amount_in*(1-bondingCurve.exit_tribute))*bondingCurve.price(bondingCurve.current_supply)) *-1

            new_supply = max(
                0,
                min(
                    bondingCurve.current_supply
                    + bondingCurve.buy(amount_out),
                    1000,
                )
            )

        new_price = bondingCurve.price(new_supply)
        
        # add them to Dataframe
        outputTable.loc[len(outputTable.index)] = [
            current_price,
            bondingCurve.current_supply,
            amount_in_parsed,
            tribute_collected_parsed,
            amount_out_parsed,
            new_price,
            new_supply,
            slippage_pct,
        ]
        # update current supply
        bondingCurve.current_supply = new_supply
    print("==================OUTPUT=====================")
    print(outputTable.head())
    # return the Dataframe
    return outputTable


def draw_bonding_curve_output(bondingCurve, x, y, steplist):

    fig = px.line(bondingCurve, x="supply (in thousands)", y="price")
    fig.add_vline(
        x=steplist.loc[0, "Current Supply"],
        line_width=1.5,
        line_dash="dash",
        line_color="red",
        annotation_text="Initial State",
        annotation_position="top",
    )
    for (index_label, step) in steplist.iterrows():
        # lines are lame, change to points
        fig.add_vline(
            x=step["New Supply"],
            line_width=1.5,
            line_dash="dash",
            line_color="red",
            annotation_text="Step " + str(index_label + 1),
            annotation_position= ("bottom" if index_label %2 == 0 else "top"),
        )


    return fig


def plot_augmented_bonding_curve( reserve_balance=100, initial_price=3, initial_supply=100, entry_tribute=0.05, exit_tribute=0.05, steps=1):
    
    bCurve = BondingCurve(reserve_balance, initial_price, initial_supply, entry_tribute, exit_tribute)
    curve_draw = bCurve.curve(bCurve.x())
    steplist= []
    if(steps=="1"):
        steplist = [[5, "TEC"], [100, "wxDai"], [10, "TEC"]]
    elif(steps=="2"):
        steplist = [[30, "wxDai"], [75, "TEC"], [30, "wxDai"]]

    
    steps_table = generate_outputs_table(bCurve, steplist)
    fig = draw_bonding_curve_output(curve_draw, "supply (in thousands)", "price", steps_table)

    return fig
    