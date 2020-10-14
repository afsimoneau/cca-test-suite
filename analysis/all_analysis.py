import plotly.express as px
import plotly.graph_objects as go
import plotly.colors
from plotly.subplots import make_subplots
import glob as glob
import pickle
import retransmission_analysis
import throughput_analysis
import rtt_analysis
import cwnd_analysis

from pathlib import Path
import os.path


cols = plotly.colors.DEFAULT_PLOTLY_COLORS
colorSwitch = {
    3: 0,
    10: 1,
    40: 2,
    180000: 3,
    600000: 4,
    2400000: 9, }

# returns a dictionary of all final_data directories
# example: dirs['bbr'] => ['./../final_data/bbr/3/',...]


def getDirs():

    init_cwnds = ['3', '10', '40']
    algos = ['bbr', 'cubic_hystart_off', 'cubic_hystart_on', 'hybla', 'pcc']

    dirs = {}

    for algo in algos:
        for init_cwnd in init_cwnds:
            if algo == 'pcc':
                init_cwnd = str(int(init_cwnd) * 60000)

            if algo not in dirs:
                dirs[algo] = []

            dirs[algo].append(Path(f'../final_data/{algo}/{init_cwnd}/'))
    return dirs


def analysis(algosToPlot, reload=False):
    dirs = getDirs()  # dirs['bbr'] => all bbr directories
    print(dirs)

    # return
    # dicts to hold all the graphs
    # index is algo, each index holds a list off all the data: cwnd['bbr'] => list bbr cwnd data
    # every element of the lists contains a tuple of the data used to make the graph then the name of the graph
    # example: cwnd['bbr'][0] => (df, '3')
    #          cwnd['bbr'][1] => (df, '10')
    #          cwnd['bbr'][2] => (df, '40')
    cwnd = {}
    throughput = {}
    rtt = {}
    retransmissions = {}

    for algo in algosToPlot:

        if os.path.isfile(f"{algo}.p") and not reload:
            cwnd[algo], throughput[algo], rtt[algo], retransmissions[algo] = pickle.load(
                open(f"{algo}.p", "rb"))

        if algo not in cwnd:
            cwnd[algo] = []
            throughput[algo] = []
            rtt[algo] = []
            retransmissions[algo] = []

            for dir in dirs[algo]:
                localPaths = list(dir.glob('**/local.csv'))
                print(localPaths)
                mlcPaths = list(dir.glob('**/*.cs.wpi.edu.csv'))
                print(mlcPaths)
                name = ' '.join(str(dir).split('/')[-1:])
                # cwnd
                cwnd[algo].append((cwnd_analysis.getAverage(dir), name))
                # throuput
                throughput[algo].append(
                    (throughput_analysis.run_throughput_analysis(localPaths), name))
                # rtt
                rtt[algo].append(
                    (rtt_analysis.run_rtt_analysis(mlcPaths), name))
                # retransmissions
                retransmissions[algo].append(
                    (retransmission_analysis.run_retransmission_analysis(localPaths), name))
        if not os.path.isfile(f"{algo}.p") or reload:
            pickle.dump((cwnd[algo], throughput[algo], rtt[algo], retransmissions[algo]),
                        open(f"{algo}.p", "wb"))

    return (cwnd, throughput, rtt, retransmissions)


def main():
    algosToPlot = [
        'bbr',
        'cubic_hystart_off',
        'cubic_hystart_on',
        'hybla',
        'pcc'
    ]

    cwnd, throughput, rtt, retransmissions = analysis(
        algosToPlot, reload=False)  # reload=true reruns the analysis and doesnt use the pickle files

    # for algo in algosToPlot:
    #     plot_algo(algo, cwnd, throughput, rtt, retransmissions)
    # plot_algo('cubic_hystart_on', cwnd, throughput, rtt, retransmissions)

    plot_algo(['bbr',
               'cubic_hystart_on',
               'hybla',
               'pcc'], cwnd, throughput, rtt, retransmissions)

    # plot_algo(['cubic_hystart_off', 'cubic_hystart_on'],
    #           cwnd, throughput, rtt, retransmissions)


def plot_algo(cca, cwnd, throughput, rtt, retransmissions):
    if not isinstance(cca, list):
        cca = [cca]

    fig = make_subplots(rows=4, cols=len(
        cca), subplot_titles=cca, shared_yaxes=True)

    legend = True

    for index, algo in enumerate(cca):
        if algo == 'pcc':
            legend = True

        for x in cwnd[algo]:
            df = x[0]
            name = x[1]

            colorIndex = colorSwitch.get(int(name))

            fig.add_trace(go.Scatter(x=df.index, y=df['mean'],
                                     mode='lines',
                                     name=name,
                                     marker=dict(color=cols[colorIndex]), showlegend=legend),
                          row=1,
                          col=index+1)
            fig.update_xaxes(
                range=[0, 60])
            fig.update_yaxes(title_text="cwnd", row=1, col=1)

        for x in throughput[algo]:
            data = x[0]
            name = x[1]

            colorIndex = colorSwitch.get(int(name))

            fig.add_trace(go.Scatter(x=data[0], y=data[1],
                                     mode='lines',
                                     name=name,
                                     marker=dict(color=cols[colorIndex]), showlegend=False),
                          row=2,
                          col=index+1)
            fig.update_xaxes(
                range=[0, 60])
            fig.update_yaxes(title_text="Throughput (MB/s)", row=2, col=1)

        for x in rtt[algo]:
            data = x[0]
            name = x[1]

            colorIndex = colorSwitch.get(int(name))

            fig.add_trace(go.Scatter(x=data[0], y=data[1],
                                     mode='lines',
                                     name=name,
                                     marker=dict(color=cols[colorIndex]), showlegend=False),
                          row=3,
                          col=index+1)
            fig.update_xaxes(
                range=[0, 60])
            fig.update_yaxes(title_text="RTT (ms)", range=[
                             0, 4000], row=3, col=1)
            # fig.update_yaxes(title_text="RTT (ms)", row=3, col=1)

        for x in retransmissions[algo]:
            data = x[0]
            name = x[1]

            colorIndex = colorSwitch.get(int(name))

            fig.add_trace(go.Scatter(x=data[0], y=data[1],
                                     mode='lines',
                                     name=name,
                                     marker=dict(color=cols[colorIndex]), showlegend=False),
                          row=4,
                          col=index+1)
            fig.update_xaxes(
                range=[0, 60])
            fig.update_yaxes(title_text="Retransmissions (%)", row=4, col=1)

            legend = False

        title = 'slow_start_initial_rate' if algo == 'pcc' and len(
            algo) == 1 else 'initcwnd'

        if len(algo) == 1:
            fig.update_layout(title=f'{algo}',
                              yaxis_title='cwnd', legend_title=title,
                              )
    fig.show()


if __name__ == "__main__":
    main()
