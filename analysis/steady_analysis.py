import os
import plotly.express as px
import pandas as pd
import time as time
import datetime as datetime

'''
ALGORITHMS = ["cubic","bbr","hybla","pcc","cubic_hystart_off"]
LETTERS = ["A","B","C","D","A"]
WINDOWS = [3,5,10,20,40,100,250]
PCC_WINDOWS = [180000,300000,600000,1200000,2400000]
'''

ALGORITHMS = {
    "cubic_cwnd":"A"}
WINDOWS = [5,10,20,40,100,250]

PERIOD = 27 #period of percent change
DELTA = 0

#takes a percet change df
def find_steady_state(df):
    mask = df["pct"] == DELTA
    return df[mask]

def main():
    os.chdir("..")
    dataPoints = pd.DataFrame(columns=["time","algo","inwin"])
    for algo,letter in ALGORITHMS.items():
        for inwin in WINDOWS:
            for i in range(5):
                path = os.path.join(os.getcwd(), 'initcwnd_data',algo,"hystart_off",str(inwin),f'mlcnet{letter}.cs.wpi.edu_cubic_{i}','cwnd.csv')
                print(path)
                df = pd.read_csv(path)
                df['pct'] = df.cwnd.pct_change(periods = PERIOD)

                #format = "%Y-%m-%d %H:%M:%S:%f"
                print(df)
                print(find_steady_state(df))
                start = pd.to_datetime(df["time"].head(1), infer_datetime_format=True)[0].to_datetime64()
                steadyData = find_steady_state(df)
                steady = pd.to_datetime(find_steady_state(df)["time"], infer_datetime_format=True).head(1)
                result = steady-start
                #rowVal = result.where["time">5]
                '''for val in result:
                    if (val.total_seconds())'''
                row = {"time":result.iloc[0].total_seconds(), "algo":algo,"inwin":inwin}
                print(row)
                dataPoints = dataPoints.append(row, ignore_index=True)
    print(dataPoints)
    figure = px.scatter(data_frame=dataPoints,x="inwin",y="time", color="algo",
    labels={"inwin":"Initial Window Size", "time":"Time (s)"}, title=f"Steady-state point")
    figure.show()




    '''TODO:
    - create plotly figure scatterplot
    - add points to plot, separating them by:
        - x-axis goes by algorithm/cwnd (pcc is algorithm/initial rate)
        - y-axis is steady state time
    - color by algorithm
    '''



if __name__ == "__main__":
    main()

