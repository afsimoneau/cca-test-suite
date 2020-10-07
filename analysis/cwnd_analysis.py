import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from glob import glob


def dateparse(x): return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')


def getAverage(dir):
    cwnds = glob(dir + '**/cwnd.csv')
    dfs = []
    for path in cwnds:
        df = pd.read_csv(path, parse_dates=[
                         'time'], date_parser=dateparse, index_col=0)
        dfs.append(df)

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


def main():
    # df = pd.read_csv(
    #     # './../initcwnd_data/cubic/100/mlcnetA.cs.wpi.edu_cubic_test_0/cwnd.csv')
    #     './../initcwnd_data/cubic_cwnd/10/mlcnetA.cs.wpi.edu_cubic_2/cwnd.csv', parse_dates=['time'], date_parser=dateparse, index_col=0)

    dir5 = './../initcwnd_data/cubic_cwnd/hystart_off/5/'
    dir10 = './../initcwnd_data/cubic_cwnd/hystart_off/10/'
    dir20 = './../initcwnd_data/cubic_cwnd/hystart_off/20/'
    dir40 = './../initcwnd_data/cubic_cwnd/hystart_off/40/'
    dir100 = './../initcwnd_data/cubic_cwnd/hystart_off/100/'
    dir250 = './../initcwnd_data/cubic_cwnd/hystart_off/100/'

    result_df5 = getAverage(dir5)
    result_df10 = getAverage(dir10)
    result_df20 = getAverage(dir20)
    result_df40 = getAverage(dir40)
    result_df100 = getAverage(dir100)
    result_df250 = getAverage(dir250)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=result_df5.index, y=result_df5['mean'],
                             mode='lines',
                             name='5'))
    fig.add_trace(go.Scatter(x=result_df10.index, y=result_df10['mean'],
                             mode='lines',
                             name='10'))
    fig.add_trace(go.Scatter(x=result_df20.index, y=result_df20['mean'],
                             mode='lines',
                             name='20'))
    fig.add_trace(go.Scatter(x=result_df40.index, y=result_df40['mean'],
                             mode='lines',
                             name='40'))
    fig.add_trace(go.Scatter(x=result_df100.index, y=result_df100['mean'],
                             mode='lines',
                             name='100'))
    fig.add_trace(go.Scatter(x=result_df250.index, y=result_df250['mean'],
                             mode='lines',
                             name='250'))

    fig.update_layout(title='Average cwnd',
                      xaxis_title='Time (s)',
                      yaxis_title='cwnd')

    fig.show()

# fig = px.line(result_df0, x=result_df0.index, y='mean')
# fig.show()

# fig = px.line(result_df1, x=result_df1.index, y='mean')
# fig.show()

# fig = px.line(result_df, x=result_df.index, y=[
#               'cwnd' + str(i) for i in range(5)])
# fig.show()

# average = pd.DataFrame()
# average['cwnd'] = df["cwnd"].resample('0.5S').mean()

# start = df.first_valid_index()

# df["delta"] = [(end - start).total_seconds()
#                for end in (df.index)]

# fig = px.line(df, x='delta', y="cwnd")

# start = average.first_valid_index()

# average["delta"] = [(end - start).total_seconds()
#                     for end in (average.index)]

# fig = px.line(average, x='delta', y="cwnd")

# fig.show()


if __name__ == "__main__":
    main()
