import os
from holoviews.element.path import Bounds
import pandas as pd
import param as pm
import panel as pn
from param.parameterized import output
import plotly.express as px
import plotly.graph_objects as go
from holoviews.plotting.plotly.dash import to_dash
import numpy as np

import dash_table
import dash_html_components as dash_html

#These numbers are fixed from the hatch results (in thousands)
TOTAL_HACTH_FUNDING = 1571.22357 
TOTAL_INITIAL_TECH_SUPPLY= 2035.918945 


class BondingCurveInitializer:

    def __init__(self, reserve_balance=100, initial_price=5, initial_supply=100):
        self.initial_price = initial_price
        self.initial_supply = initial_supply
        self.initial_balance = reserve_balance

    def reserve_ratio(self):
        return self.initial_balance / (self.initial_price * self.initial_supply)
    
    #Returns the token price given a specific supply
    def get_price(self, supply):
        return (supply ** ((1 / self.reserve_ratio()) - 1) * self.initial_price) / (
            self.initial_supply ** ((1 / self.reserve_ratio()) - 1)
        )

    #Returns the collateral balance price given a specific supply
    def get_balance(self, supply):
        return (
            self.reserve_ratio() * self.get_price(supply) * supply
        )

    #Returns supply at a specific balance. THIS IS AN APPROXIMATION only meant for visualizing scenarios
    def get_supply(self, balance):
        supply_ref = 0
        while self.get_balance(supply_ref) <  balance:
            supply_ref = supply_ref + 10

        df = self.curve_over_balance(supply_ref-10, supply_ref, 10000)
        df_rounded = df.round(3)
        
        index= df.index.where(df_rounded['Balance (in thousands)'] >= balance).dropna()[0]
        price = df.at[index, "Price"]

        supply = balance/(price* self.reserve_ratio())
        

        return supply

    #For drawing the bonding curve. Range shows how many times the initial supply you make the graph for, steps how many subdivisions
    def curve_over_supply(self, range_begin=0, range_end=1000, steps=1000):
        x = np.linspace(range_begin, range_end, steps)
        y = self.get_price(x)

        return pd.DataFrame(zip(x, y), columns=["Supply (in thousands)", "Price"])
    
    def curve_over_balance(self, range_begin=0, range_end=1000, steps=1000):
        supply_list = np.linspace(range_begin, range_end, steps)
        x = self.get_balance(supply_list)
        y = self.get_price(supply_list)

        return pd.DataFrame(zip(x, y), columns=["Balance (in thousands)", "Price"])



class BondingCurve(BondingCurveInitializer):

    def __init__(self, reserve_balance=100, initial_price=5, initial_supply=100, entry_tribute=0.05, exit_tribute=0.05):
        super().__init__(reserve_balance, initial_price, initial_supply)
        self.current_supply = self.initial_supply
        self.current_balance = self.get_balance(self.initial_supply)
        self.entry_tribute = entry_tribute
        self.exit_tribute = exit_tribute

    def set_new_supply(self, new_supply):
        self.current_supply = new_supply
        self.current_balance = self.get_balance(new_supply)

    #Returns how much wxDai you get from selling TEC. Informative, doesn't change state
    def sale_return(self, bonded):
        return self.current_balance * (
            (bonded / self.current_supply + 1) ** (1 / self.reserve_ratio()) - 1
        )

    #Returns how much TEC you get from purchasing with wxDai. Informative, doesn't change state
    def purchase_return(self, collateral):
        return self.current_supply * (
            (collateral / self.current_balance + 1) ** (self.reserve_ratio()) - 1
        )



class BondingCurveHandler():
    '''
    The handler for the Bonding Curve. All interaction happens through this.

    The constrctor receives following args:

    hatch_funding: Number in thousands (100 -> 100k). Total of funds collected BEFORE applying tribute. For now doubles as total supply
    commons_percentage: int between 0-95. Percentage of funds that get substracted from the total funding to go to the commons pool
    initial_price: float. No real limit but, expected to be between 1 and 4
    entry_tribute: int between 0-99. Percentage of funds substracted on buy (mint) operations before interacting with the bonding curve
    exit_tribute: int between 0-99. Percentage of funds substracted on sell (burn) operations after interacting with the boding curve
    steplist: list with format [["AMOUNT", "TOKEN"],["AMOUNT", "TOKEN"]]. Set of buy/sell operations applied to the bonding curve.
    zoom_graph=0: optional. value 0 or 1. To specify if the draw function should show the whole curve(0) or "zoom in" into the area where operations are happening (1)
    plot_mode=0: optional. value 0 or 1. Not in the scope of this iteration. Specifies if the draw function should plot the price against the balance (0) or the supply (1)
    
    '''

    def __init__(self,
                 commons_percentage,
                 ragequit_percentage,
                 initial_price,
                 entry_tribute,
                 exit_tribute,
                 hatch_scenario_funding,
                 steplist,
                 zoom_graph=0,
                 plot_mode=0):
        #
        #check here for validity of parameters
        #
        params_valid = self.check_param_validity( 
                 commons_percentage,
                 ragequit_percentage,
                 initial_price,
                 entry_tribute,
                 exit_tribute,
                 float(hatch_scenario_funding),
                 steplist,
                 int(zoom_graph),
                 int(plot_mode)
                 )
        #The numbers for initial supply and taken from the constants
        self.bonding_curve = self.create_bonding_curve(commons_percentage=commons_percentage, ragequit_percentage=ragequit_percentage, initial_price=initial_price, entry_tribute= entry_tribute / 100, exit_tribute= exit_tribute / 100)
        
        #set the current supply to the point where the scenarios are going to happen
        if(float(hatch_scenario_funding) != TOTAL_HACTH_FUNDING):
            print("enter")
            scenario_supply= self.bonding_curve.get_supply(float(hatch_scenario_funding))
            self.bonding_curve.set_new_supply(scenario_supply)
        
        self.steps_table = self.generate_outputs_table(bondingCurve= self.bonding_curve, steplist= steplist)
        self.zoom_graph = zoom_graph
        self.plot_mode = plot_mode
    
    #switch commented part depending on the output wanted: first more formatted, second raw
    def get_data(self):
        
        figure_bonding_curve = self.get_data_augmented_bonding_curve(bondingCurve= self.bonding_curve, steps_table= self.steps_table, zoom_graph=self.zoom_graph, plot_mode=self.plot_mode)
        figure_buy_sell_table = self.get_data_table(self.steps_table)

        #figure_bonding_curve = self.get_data_augmented_bonding_curve(bondingCurve= self.bonding_curve, steps_table= self.steps_table, zoom_graph=self.zoom_graph, plot_mode=self.plot_mode)
        #figure_buy_sell_table = self.steps_table.loc[:,["Step", "Current Price", "Amount in", "Tribute collected", "Amount out", "New Price", "Slippage"]].to_dict(orient='list')

        return figure_bonding_curve, figure_buy_sell_table

    def create_bonding_curve(self, commons_percentage=50, ragequit_percentage=5,  initial_price=3, entry_tribute=0.05, exit_tribute=0.05):
        
        initial_supply = TOTAL_INITIAL_TECH_SUPPLY * (1 - (ragequit_percentage/100))
        hatch_funding= TOTAL_HACTH_FUNDING * (1 - (ragequit_percentage/100))

        initial_reserve = hatch_funding - (hatch_funding * (commons_percentage/100))
        
        bCurve = BondingCurve(initial_reserve, initial_price, initial_supply, entry_tribute, exit_tribute)

        return bCurve

    def generate_outputs_table(self, bondingCurve, steplist):

        column_names = [
            "Step",
            "Current Price",
            "Current Supply",
            "Current Balance",
            "Amount in",
            "Tribute collected",
            "Amount out",
            "New Price",
            "New Supply",
            "New Balance",
            "Slippage",
        ]
        outputTable = pd.DataFrame(columns=column_names)

        for index, step in enumerate(steplist):

            current_price = bondingCurve.get_price(bondingCurve.current_supply)

            amount_in = step[0]
            amount_in_parsed = str(format(amount_in, '.2f')) + " " + str(step[1])
        
            amount_out = 0
            amount_out_parsed = ""
            new_supply = 0
            tribute_collected = 0
            if step[1] == "wxDai":
                # take tribute and buy
                tribute_collected = amount_in * bondingCurve.entry_tribute
                amountAfterTribute = amount_in - tribute_collected

                amount_out = bondingCurve.purchase_return(amountAfterTribute)
                amount_out_parsed = str(format(amount_out, '.2f')) + " TEC"
                tribute_collected_parsed = str(format(tribute_collected, '.2f')) + " wxDai"

                slippage = (amount_in - tribute_collected)/bondingCurve.get_price(bondingCurve.current_supply) - amount_out
                slippage_pct = slippage / ((amount_in - tribute_collected)/bondingCurve.get_price(bondingCurve.current_supply))
                slippage_pct = str(format((slippage_pct*100), '.2f')) + "%"

                new_supply = max(
                    0, bondingCurve.current_supply + amount_out
                )
            elif step[1] == "TEC":
                #this section works, but all the -1 mults are a bit of a mess. 
                # sell and take tribute
                amount_in = amount_in * -1 #because we are reducing the supply (burning)
                amountBeforeTribute = bondingCurve.sale_return(amount_in)            

                tribute_collected = amountBeforeTribute * bondingCurve.exit_tribute #since it is a sale, the number returned is negative
                tribute_collected_parsed = str(format((tribute_collected*-1), '.2f')) + " wxDai"
                amount_out = (amountBeforeTribute - tribute_collected) #we leave it negative for the supply calculations down below
                amount_out_parsed = str(format((amount_out*-1), '.2f')) + " wxDai" 

                slippage = ((amount_in*(1-bondingCurve.exit_tribute))*bondingCurve.get_price(bondingCurve.current_supply) - amount_out) *-1
                slippage_pct = slippage / ((amount_in*(1-bondingCurve.exit_tribute))*bondingCurve.get_price(bondingCurve.current_supply)) *-1
                slippage_pct = str(format((slippage_pct*100), '.2f')) + "%"

                new_supply = max(
                    0, bondingCurve.current_supply + bondingCurve.purchase_return(amount_out),
                )

            new_price = bondingCurve.get_price(new_supply)
            new_balance = bondingCurve.get_balance(new_supply)

            # add to Dataframe
            outputTable.loc[len(outputTable.index)] = [
                (index+1),
                round(current_price, 2),
                round(bondingCurve.current_supply, 2),
                round(bondingCurve.current_balance, 2),
                amount_in_parsed,
                tribute_collected_parsed,
                amount_out_parsed,
                round(new_price, 2),
                round(new_supply, 2),
                round(new_balance, 2),
                slippage_pct,
            ]

            # update current supply and balance 
            bondingCurve.set_new_supply(new_supply)

        #print("==================OUTPUT=====================")
        #print(outputTable.head())

        return outputTable

    def draw_bonding_curve_output(self, bondingCurve, x, y, steps_table, plot_mode=0):

        col_current= "Current Supply" if plot_mode == "1" else "Current Balance"
        col_new = "New Supply" if plot_mode == "1" else "New Balance"

        fig = px.line(bondingCurve, x, y)
        fig.add_vline(
            x=steps_table.loc[0, col_current],
            line_width=1.5,
            line_dash="dash",
            line_color="red",
            annotation_text="Initial State",
            annotation_position="top",
        )
        for (index_label, step) in steps_table.iterrows():
            # lines are lame, change to points
            fig.add_vline(
                x=step[col_new],
                line_width=1.5,
                line_dash="dash",
                line_color="red",
                annotation_text="Step " + str(index_label + 1),
                annotation_position= ("bottom" if index_label %2 == 0 else "top"),
            )


        return fig

    def get_data_augmented_bonding_curve(self, bondingCurve, steps_table, zoom_graph="0", plot_mode="0"):
        
        min_range = 0 if  zoom_graph == "0" else ( min(steps_table['Current Supply'].min(), steps_table['New Supply'].min()) - 50)
        max_range = steps_table['New Supply'].max() + (200 if zoom_graph == "0" else 50)

        #switch commented part depending on the output you want
        if plot_mode == 0:
            curve_draw = bondingCurve.curve_over_balance(min_range, max_range)
            fig = self.draw_bonding_curve_output(curve_draw, "Balance (in thousands)", "Price", steps_table, plot_mode=plot_mode)
        elif plot_mode == 1:
            curve_draw = bondingCurve.curve_over_supply(min_range, max_range)
            fig = self.draw_bonding_curve_output(curve_draw, "Supply (in thousands)", "Price", steps_table, plot_mode=plot_mode)
        '''
        if plot_mode == "0":
            curve_draw = bondingCurve.curve_over_balance(min_range, max_range)
        elif plot_mode == "1":
            curve_draw = bondingCurve.curve_over_supply(min_range, max_range)
        '''

        return fig
        #return curve_draw

    def check_param_validity(self, commons_percentage, ragequit_percentage, initial_price, entry_tribute, exit_tribute,  hatch_scenario_funding,  steplist, zoom_graph, plot_mode):
        if hatch_scenario_funding <= 0:
            raise ValueError("Error: Invalid  Hatch Scenario Funding Parameter.")
        if commons_percentage < 0 or commons_percentage > 95:
            raise ValueError("Error: Invalid Commons Percentage Parameter.")
        if ragequit_percentage < 0 or ragequit_percentage > 20:
            raise ValueError("Error: Invalid Ragequit Percentage Parameter.")
        if initial_price <=0:
            raise ValueError("Error: Invalid Initial Price Parameter.")
        if entry_tribute < 0 or entry_tribute >= 100:
            raise ValueError("Error: Invalid Entry Tribute Parameter.")
        if exit_tribute < 0 or exit_tribute >= 100:
            raise ValueError("Error: Invalid Exit Tribute Parameter.")
        if not isinstance(steplist, list):
            raise ValueError("Error: Invalid Steplist Parameter.")
        if not (zoom_graph == 0 or zoom_graph == 1):
            raise ValueError("Error: Invalid Graph Zoom Parameter.")
        if not (plot_mode == 0 or plot_mode == 1):
            raise ValueError("Error: Invalid Plot Mode Parameter.")
        
        return True
        

    def get_data_table(self, steps_table):

        steps_table = steps_table.loc[:,["Step", "Current Price", "Amount in", "Tribute collected", "Amount out", "New Price", "Slippage"]]

        data = steps_table.to_dict("records")
        cols = [{"name": i, "id": i} for i in steps_table.columns]

        data_table = dash_html.Div([
                        dash_table.DataTable(
                                        id='table',
                                        data=data, 
                                        columns=cols,
                                        style_cell={'width': '50px',
                                                    'height': '30px',
                                                    'textAlign': 'left'}
                                            )
                                ])
        return data_table
    