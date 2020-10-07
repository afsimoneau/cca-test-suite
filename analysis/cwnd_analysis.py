import plotly.express as px
import pandas as pd
from datetime import datetime
def dateparse(x): return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')


def main():
    df = pd.read_csv(
        # './../initcwnd_data/cubic_test/10/mlcnetA.cs.wpi.edu_cubic_test_0/cwnd.csv')
        './../initcwnd_data/cubic_test/10/mlcnetA.cs.wpi.edu_cubic_test_0/cwnd.csv', parse_dates=['time'], date_parser=dateparse, index_col=0)

    print(df)

    average = pd.DataFrame()
    average['cwnd'] = df["cwnd"].resample('0.5S').mean()

    start = average.first_valid_index()

    average["delta"] = [(end - start).total_seconds()
                        for end in (average.index)]

    fig = px.line(average, x='delta', y="cwnd")

    fig.show()


if __name__ == "__main__":
    main()

