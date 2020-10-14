import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from glob import glob
from pathlib import Path


def dateparse(x): return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')


def getAverage(dir):
    cwnds = list(dir.glob('**/cwnd.csv'))
    for file1 in cwnds:
        f = open(file1, 'r+')
        lines = f.readlines()  # read old content
        # print(file1)
        if "time" not in lines[0]:
            print("replace")
            f.seek(0)  # go back to the beginning of the file
            f.write("time,cwnd\n")  # write new content at the beginning
            for line in lines:  # write old content after new
                f.write(line)
            f.close()

    dfs = []
    for path in cwnds:
        print(path)
        df = pd.read_csv(path, parse_dates=[
                         'time'], date_parser=dateparse, index_col=0)
        dfs.append(df)

    # print(dfs)
    average_dfs = []

    for df in dfs:
        average = pd.DataFrame()
        average['cwnd'] = df["cwnd"].resample('0.5S').mean()
        start = average.first_valid_index()
        average["delta"] = [(end - start).total_seconds()
                            for end in (average.index)]

        average_dfs.append(average)

    # print(average_dfs)

    # find the smallest max time
    minMax = 1000000
    for df in average_dfs:
        currMax = df['delta'].max()
        if currMax < minMax:
            minMax = currMax
            # print(currMax)

    # drop rows greater than the minMax
    result_df = None
    for index, df in enumerate(average_dfs):
        average_dfs[index] = df[df['delta'] <=
                                minMax].set_index('delta').rename(columns={'cwnd': 'cwnd'+str(index)})
        if index is 0:
            result_df = average_dfs[index]
        else:
            result_df['cwnd' + str(index)
                      ] = average_dfs[index]['cwnd' + str(index)]
    result_df['mean'] = result_df.mean(axis=1)

    return result_df
