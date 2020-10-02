import csv
import plotly
import sys
import os
from glob import glob

def parse_csv(csv_file):
    data_points = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    previous_bytes = 0
    start_time = None
    for row in csv_reader:
        if line_count == 0:
            pass
        else:
            if row[4] != "192.168.1.102":
                if start_time == None:
                    start_time = sum(x * float(t) for x, t in zip([3600, 60, 1], row[11][12:30].split(":")))
                    data_points.append([0,0,0])
                elif int(row[8]) > previous_bytes:
                    data_points.append([1,0,sum(x * float(t) for x, t in zip([3600, 60, 1], row[11][12:30].split(":"))) - start_time])
                    previous_bytes = int(row[8])
                elif int(row[8]) <= previous_bytes and int(row[8]) > 10:
                    data_points.append([0,1,sum(x * float(t) for x, t in zip([3600, 60, 1], row[11][12:30].split(":"))) - start_time])

        line_count += 1
    return data_points

def totals_per_time_frame(data_points, time_frame):
    time_frame_min = 0
    time_frame_max = time_frame
    percent_retransmissions_list = []
    time_list = []
    transmissions_in_frame = 0
    retransmissions_in_frame = 0
    index = 0
    while time_frame_max < data_points[-1][2] and index < len(data_points):
        if data_points[index][2] >= time_frame_min and data_points[index][2] < time_frame_max:
            transmissions_in_frame += data_points[index][0] + data_points[index][1]
            retransmissions_in_frame += data_points[index][1]
            index += 1
        else:
            try:
                percent_retransmissions = 100*retransmissions_in_frame/transmissions_in_frame
            except ZeroDivisionError:
                percent_retransmissions = 0
            percent_retransmissions_list.append(percent_retransmissions)
            time_list.append(time_frame_min)
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            transmissions_in_frame = 0
            retransmissions_in_frame = 0
    
    return [percent_retransmissions_list,time_list]
    
def generate_trace(csv_files, figure):
    data_points = []
    for x in csv_files:
        data_points = parse_csv(open(x))
        data_points = totals_per_time_frame(data_points, time_frame)
        # print(data_points)
        figure.add_trace(plotly.graph_objects.Scatter(
            x=data_points[1],
            y=data_points[0],
        ))

time_frame = 1
fig3 = plotly.graph_objects.Figure()
fig5 = plotly.graph_objects.Figure()
fig10 = plotly.graph_objects.Figure()
fig20 = plotly.graph_objects.Figure()
fig40 = plotly.graph_objects.Figure()

cubic = [[".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
          ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
          ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
          ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
          ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"],
         [".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
          ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
          ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
          ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
          ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"],\
         [".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
          ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
          ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
          ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
          ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"],\
         [".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
          ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
          ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
          ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
          ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"],\
         [".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
          ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
          ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
          ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
          ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]]

generate_trace(cubic[0],fig3)
generate_trace(cubic[1],fig5)
generate_trace(cubic[2],fig10)
generate_trace(cubic[3],fig20)
generate_trace(cubic[4],fig40)

fig3.update_layout(title="Cubic 3", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
fig3.show()

fig5.update_layout(title="Cubic 5", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
fig5.show()

fig10.update_layout(title="Cubic 10", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
fig10.show()

fig20.update_layout(title="Cubic 20", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
fig20.show()

fig40.update_layout(title="Cubic 40", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
fig40.show()
