import os
import plotly.express as px
import pandas as pd


ALGORITHMS = ["cubic","bbr","hybla","pcc","cubic_hystart_off"]
LETTERS = ["A","B","C","D","A"]
WINDOWS = [3,5,10,20,40,100,250]
PCC_WINDOWS = [180000,300000,600000,1200000,2400000]

def find_steady_state_point(percent_change):
    for x in percent_change:
        if (-.001<x<.001):
            return x #might want to print this to see what you get

def main():
    print("main")
    '''TODO:
    - read CSV data into DataFrames
    - calculate steady state points (store in DataFrame)
    - create plotly figure scatterplot
    - add points to plot, separating them by:
        - x-axis goes by algorithm/cwnd (pcc is algorithm/initial rate)
        - y-axis is steady state time
    - color by algorithm
    '''



if __name__ == "__main__":
    main()

