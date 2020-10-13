import plotly.express as px
import plotly.graph_objects as go
import plotly.colors
from plotly.subplots import make_subplots
from pathlib import Path

import cwnd_analysis

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


def main():
    algosToPlot = [
        'bbr',
        # 'cubic_hystart_off',
        'cubic_hystart_on',
        'hybla',
        'pcc'
    ]

    dirs = getDirs()  # dirs['bbr'] => all bbr directories
    print(dirs)

    # return
    # dicts to hold all the graphs
    # index is algo, each index holds a list off all the data: cwnd['bbr'] => list bbr cwnd data
    # every element of the lists contains a tuple of the data used to make the graph then the name of the graph
    # example: cwnd['bbr'][0] => (df, 'bbr 3')
    #          cwnd['bbr'][1] => (df, 'bbr 10')
    #          cwnd['bbr'][2] => (df, 'bbr 40')
    cwnd = {}
    throughput = {}
    rtt = {}
    retransmissions = {}

    for algo in algosToPlot:
        if algo not in cwnd:
            cwnd[algo] = []
            throughput[algo] = []
            rtt[algo] = []
            retransmissions[algo] = []

            for dir in dirs[algo]:
                name = ' '.join(str(dir).split('/')[-1:])
                # cwnd
                cwnd[algo].append((cwnd_analysis.getAverage(dir), name))
                # throuput
                # rtt
                # retransmissions

    fig = make_subplots(rows=1, cols=len(algosToPlot),
                        subplot_titles=algosToPlot)

    cols = plotly.colors.DEFAULT_PLOTLY_COLORS
    colorSwitch = {
        3: 0,
        10: 1,
        40: 2,
        180000: 3,
        600000: 4,
        2400000: 9, }
    legend = True
    for index, algo in enumerate(algosToPlot):
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
        legend = False

    fig.update_layout(title=f'Average cwnd',
                      xaxis_title='Time (s)',
                      yaxis_title='cwnd')
    fig.show()


if __name__ == "__main__":
    main()
