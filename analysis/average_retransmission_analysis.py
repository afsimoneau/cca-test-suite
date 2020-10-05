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
            percent_retransmissions_list.append([percent_retransmissions,time_frame_min])
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            transmissions_in_frame = 0
            retransmissions_in_frame = 0
    return percent_retransmissions_list

def average_data(data_points, time_frame):
    time_frame_min = 0
    time_frame_max = time_frame
    avg_mbits_per_second_list = []
    seconds_list = []
    mbits_in_frame = 0
    samples = 0
    index = 0
    while time_frame_max < data_points[-1][1] and index < len(data_points):
        if data_points[index][1] >= time_frame_min and data_points[index][1] < time_frame_max:
            mbits_in_frame += data_points[index][0]
            samples += 1
            index += 1
        else:
            try:
                avg_mbits = mbits_in_frame/samples
                avg_mbits_per_second = avg_mbits/time_frame
                avg_mbits_per_second_list.append(avg_mbits_per_second)
            except ZeroDivisionError:
                avg_mbits_per_second_list.append(0)
            seconds_list.append(time_frame_min)
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            mbits_in_frame = 0
            samples = 0
    return [avg_mbits_per_second_list,seconds_list]
    
def generate_trace(csv_files_to_average, label, figure):
    total_data_points = []
    data_points = []
    averaged_lists = []

    for x in csv_files_to_average:
        data_points = parse_csv(open(x))
        data_points = totals_per_time_frame(data_points, time_frame)
        for y in data_points:
            total_data_points.append(y)

    total_data_points = sorted(total_data_points,key=lambda x: x[1])
    averaged_lists = average_data(total_data_points, time_frame)

    figure.add_trace(plotly.graph_objects.Scatter(
        x=averaged_lists[1],
        y=averaged_lists[0],
        name=label  
    ))

time_frame = 1
fig_cubic5 = plotly.graph_objects.Figure()
fig_cubic7 = plotly.graph_objects.Figure()

cubic5 = [[".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
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

cubic7 = [[".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
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
          ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"],\
         [".\\initcwnd_data\\cubic\\100\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
          ".\\initcwnd_data\\cubic\\100\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
          ".\\initcwnd_data\\cubic\\100\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
          ".\\initcwnd_data\\cubic\\100\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
          ".\\initcwnd_data\\cubic\\100\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"],\
         [".\\initcwnd_data\\cubic\\250\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
          ".\\initcwnd_data\\cubic\\250\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
          ".\\initcwnd_data\\cubic\\250\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
          ".\\initcwnd_data\\cubic\\250\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
          ".\\initcwnd_data\\cubic\\250\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]]

names = ["3","5","10","20","40","100","250"]
index = 0


for inwin in cubic5:
    generate_trace(inwin,names[index],fig_cubic5)
    index += 1

index = 0

for inwin in cubic7:
    generate_trace(inwin,names[index],fig_cubic7)
    index += 1


fig_cubic5.update_layout(title="Average Retransmission Rate: Cubic (5 traces)", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
fig_cubic5.show()

fig_cubic7.update_layout(title="Average Retransmission Rate: Cubic (7 traces)", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
fig_cubic7.show()


