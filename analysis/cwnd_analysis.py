import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from glob import glob


def dateparse(x): return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')


def getAverage(dir):
    cwnds = glob(dir + '**/cwnd.csv')
    for file1 in cwnds:
        f = open(file1, 'r+')
        lines = f.readlines()  # read old content
        print(file1)
        if "time" not in lines[0]:
            print("replace")
            f.seek(0)  # go back to the beginning of the file
            f.write("time,cwnd\n")  # write new content at the beginning
            for line in lines:  # write old content after new
                f.write(line)
            f.close()
    # return
    dfs = []
    for path in cwnds:
        print(path)
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

    dir3_on = './../initcwnd_data/cubic_cwnd/hystart_on/3/'
    dir10_on = './../initcwnd_data/cubic_cwnd/hystart_on/10/'
    dir40_on = './../initcwnd_data/cubic_cwnd/hystart_on/40/'

    dir3_off = './../initcwnd_data/cubic_cwnd/hystart_off/3/'
    dir10_off = './../initcwnd_data/cubic_cwnd/hystart_off/10/'
    dir40_off = './../initcwnd_data/cubic_cwnd/hystart_off/40/'

    result_df3_on = getAverage(dir3_on)
    result_df10_on = getAverage(dir10_on)
    result_df40_on = getAverage(dir40_on)

    result_df3_off = getAverage(dir3_off)
    result_df10_off = getAverage(dir10_off)
    result_df40_off = getAverage(dir40_off)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=result_df3_on.index, y=result_df3_on['mean'],
                             mode='lines',
                             name='3 hystart on'))
    fig.add_trace(go.Scatter(x=result_df10_on.index, y=result_df10_on['mean'],
                             mode='lines',
                             name='10 hystart on'))
    fig.add_trace(go.Scatter(x=result_df40_on.index, y=result_df40_on['mean'],
                             mode='lines',
                             name='40 hystart on'))

    # fig.add_trace(go.Scatter(x=result_df3_off.index, y=result_df3_off['mean'],
    #                          mode='lines',
    #                          name='3 hystart off'))
    # fig.add_trace(go.Scatter(x=result_df10_off.index, y=result_df10_off['mean'],
    #                          mode='lines',
    #                          name='10 hystart off'))
    # fig.add_trace(go.Scatter(x=result_df40_off.index, y=result_df40_off['mean'],
    #                          mode='lines',
    #                          name='40 hystart off'))

    fig.update_layout(title='Average CWND Cubic Hystart On',
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
