import plotly.express as px
import plotly.graph_objects as go

import cwnd_analysis


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

            dirs[algo].append(f'./../final_data/{algo}/{init_cwnd}/')
    return dirs


def main():
    algosToPlot = [
        'bbr',
        'cubic_hystart_off',
        'cubic_hystart_on',
        'hybla',
        'pcc'
    ]

    dirs = getDirs()

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
                name = ' '.join(dir.split('/')[-3:-1])
                # cwnd
                cwnd[algo].append((cwnd_analysis.getAverage(dir), name))
                # throuput
                # rtt
                # retransmissions

    fig = go.Figure()

    for x in cwnd['pcc']:
        df = x[0]
        name = x[1]
        fig.add_trace(go.Scatter(x=df.index, y=df['mean'],
                                 mode='lines',
                                 name=name))
    fig.show()


if __name__ == "__main__":
    main()
