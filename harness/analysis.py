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
                    data_points.append([0,0])
                elif int(row[8]) >= previous_bytes:
                    data_points.append([(int(row[8])-previous_bytes),sum(x * float(t) for x, t in zip([3600, 60, 1], row[11][12:30].split(":"))) - start_time])
                    previous_bytes = int(row[8])
        line_count += 1
    return data_points

def totals_per_time_frame(data_points, time_frame):
    time_frame_min = 0
    time_frame_max = time_frame
    total_mbits_list = []
    bytes_in_frame = 0
    index = 0
    while time_frame_max < data_points[-1][1] and index < len(data_points):
        if data_points[index][1] >= time_frame_min and data_points[index][1] < time_frame_max:
            bytes_in_frame += data_points[index][0]
            index += 1
        else:
            total_megabits = 8*bytes_in_frame/1000000
            total_mbits_list.append([total_megabits,time_frame_min])
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            bytes_in_frame = 0
    return total_mbits_list

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
fig_cubic = plotly.graph_objects.Figure()
fig_bbr = plotly.graph_objects.Figure()
fig_hybla = plotly.graph_objects.Figure()

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

bbr = [[".\\initcwnd_data\\bbr\\3\\mlcnetB.cs.wpi.edu_bbr_0\\local.csv",\
          ".\\initcwnd_data\\bbr\\3\\mlcnetB.cs.wpi.edu_bbr_1\\local.csv",\
          ".\\initcwnd_data\\bbr\\3\\mlcnetB.cs.wpi.edu_bbr_2\\local.csv",\
          ".\\initcwnd_data\\bbr\\3\\mlcnetB.cs.wpi.edu_bbr_3\\local.csv",\
          ".\\initcwnd_data\\bbr\\3\\mlcnetB.cs.wpi.edu_bbr_4\\local.csv"],
        [".\\initcwnd_data\\bbr\\5\\mlcnetB.cs.wpi.edu_bbr_0\\local.csv",\
          ".\\initcwnd_data\\bbr\\5\\mlcnetB.cs.wpi.edu_bbr_1\\local.csv",\
          ".\\initcwnd_data\\bbr\\5\\mlcnetB.cs.wpi.edu_bbr_2\\local.csv",\
          ".\\initcwnd_data\\bbr\\5\\mlcnetB.cs.wpi.edu_bbr_3\\local.csv",\
          ".\\initcwnd_data\\bbr\\5\\mlcnetB.cs.wpi.edu_bbr_4\\local.csv"],
        [".\\initcwnd_data\\bbr\\10\\mlcnetB.cs.wpi.edu_bbr_0\\local.csv",\
          ".\\initcwnd_data\\bbr\\10\\mlcnetB.cs.wpi.edu_bbr_1\\local.csv",\
          ".\\initcwnd_data\\bbr\\10\\mlcnetB.cs.wpi.edu_bbr_2\\local.csv",\
          ".\\initcwnd_data\\bbr\\10\\mlcnetB.cs.wpi.edu_bbr_3\\local.csv",\
          ".\\initcwnd_data\\bbr\\10\\mlcnetB.cs.wpi.edu_bbr_4\\local.csv"],\
         [".\\initcwnd_data\\bbr\\20\\mlcnetB.cs.wpi.edu_bbr_0\\local.csv",\
          ".\\initcwnd_data\\bbr\\20\\mlcnetB.cs.wpi.edu_bbr_1\\local.csv",\
          ".\\initcwnd_data\\bbr\\20\\mlcnetB.cs.wpi.edu_bbr_2\\local.csv",\
          ".\\initcwnd_data\\bbr\\20\\mlcnetB.cs.wpi.edu_bbr_3\\local.csv",\
          ".\\initcwnd_data\\bbr\\20\\mlcnetB.cs.wpi.edu_bbr_4\\local.csv"],\
         [".\\initcwnd_data\\bbr\\40\\mlcnetB.cs.wpi.edu_bbr_0\\local.csv",\
          ".\\initcwnd_data\\bbr\\40\\mlcnetB.cs.wpi.edu_bbr_1\\local.csv",\
          ".\\initcwnd_data\\bbr\\40\\mlcnetB.cs.wpi.edu_bbr_2\\local.csv",\
          ".\\initcwnd_data\\bbr\\40\\mlcnetB.cs.wpi.edu_bbr_3\\local.csv",\
          ".\\initcwnd_data\\bbr\\40\\mlcnetB.cs.wpi.edu_bbr_4\\local.csv"]]

hybla = [[".\\initcwnd_data\\hybla\\3\\mlcnetC.cs.wpi.edu_hybla_0\\local.csv",\
          ".\\initcwnd_data\\hybla\\3\\mlcnetC.cs.wpi.edu_hybla_1\\local.csv",\
          ".\\initcwnd_data\\hybla\\3\\mlcnetC.cs.wpi.edu_hybla_2\\local.csv",\
          ".\\initcwnd_data\\hybla\\3\\mlcnetC.cs.wpi.edu_hybla_3\\local.csv",\
          ".\\initcwnd_data\\hybla\\3\\mlcnetC.cs.wpi.edu_hybla_4\\local.csv"],
        [".\\initcwnd_data\\hybla\\5\\mlcnetC.cs.wpi.edu_hybla_0\\local.csv",\
          ".\\initcwnd_data\\hybla\\5\\mlcnetC.cs.wpi.edu_hybla_1\\local.csv",\
          ".\\initcwnd_data\\hybla\\5\\mlcnetC.cs.wpi.edu_hybla_2\\local.csv",\
          ".\\initcwnd_data\\hybla\\5\\mlcnetC.cs.wpi.edu_hybla_3\\local.csv",\
          ".\\initcwnd_data\\hybla\\5\\mlcnetC.cs.wpi.edu_hybla_4\\local.csv"],
        [".\\initcwnd_data\\hybla\\10\\mlcnetC.cs.wpi.edu_hybla_0\\local.csv",\
          ".\\initcwnd_data\\hybla\\10\\mlcnetC.cs.wpi.edu_hybla_1\\local.csv",\
          ".\\initcwnd_data\\hybla\\10\\mlcnetC.cs.wpi.edu_hybla_2\\local.csv",\
          ".\\initcwnd_data\\hybla\\10\\mlcnetC.cs.wpi.edu_hybla_3\\local.csv",\
          ".\\initcwnd_data\\hybla\\10\\mlcnetC.cs.wpi.edu_hybla_4\\local.csv"],\
         [".\\initcwnd_data\\hybla\\20\\mlcnetC.cs.wpi.edu_hybla_0\\local.csv",\
          ".\\initcwnd_data\\hybla\\20\\mlcnetC.cs.wpi.edu_hybla_1\\local.csv",\
          ".\\initcwnd_data\\hybla\\20\\mlcnetC.cs.wpi.edu_hybla_2\\local.csv",\
          ".\\initcwnd_data\\hybla\\20\\mlcnetC.cs.wpi.edu_hybla_3\\local.csv",\
          ".\\initcwnd_data\\hybla\\20\\mlcnetC.cs.wpi.edu_hybla_4\\local.csv"],\
         [".\\initcwnd_data\\hybla\\40\\mlcnetC.cs.wpi.edu_hybla_0\\local.csv",\
          ".\\initcwnd_data\\hybla\\40\\mlcnetC.cs.wpi.edu_hybla_1\\local.csv",\
          ".\\initcwnd_data\\hybla\\40\\mlcnetC.cs.wpi.edu_hybla_2\\local.csv",\
          ".\\initcwnd_data\\hybla\\40\\mlcnetC.cs.wpi.edu_hybla_3\\local.csv",\
          ".\\initcwnd_data\\hybla\\40\\mlcnetC.cs.wpi.edu_hybla_4\\local.csv"]]

names = ["3","5","10","20","40" ]
index = 0

CCA_DIRS = [
    './initcwnd_data/cubic',
    './initcwnd_data/bbr',
    './initcwnd_data/hybla'
    ]

WIN_DIR = [3,5,10,20,40]
RUN_DIRS = {
    CCA_DIRS[0]:'/mlcnetA.cs.wpi.edu_cubic_',
    CCA_DIRS[1]:'/mlcnetB.cs.wpi.edu_bbr_',
    CCA_DIRS[2]:'/mlcnetC.cs.wpi.edu_hybla_'
}

if (len(sys.argv)==4):
    num_trials = int(sys.argv[3])
    mlc_letter = sys.argv[2]
    algorithm = sys.argv[1]
    figure = plotly.graph_objects.Figure()
    
    for inwin in WIN_DIR:
        paths = []
        for trial in range(num_trials):
            paths.append(f"{os.getcwd()}/initcwnd_data/{algorithm}/{inwin}/mlcnet{mlc_letter}.cs.wpi.edu_{algorithm}_{trial}/local.csv")
        print(paths)
        generate_trace(paths,inwin,figure)
        figure.update_layout(title=algorithm, xaxis_title="Time (s)", yaxis_title="Throughput (Mb/s)")
else:
    for inwin in cubic:
        generate_trace(inwin,names[index],fig_cubic)
    index += 1

    index = 0

    for inwin in bbr:
        generate_trace(inwin,names[index],fig_bbr)
        index += 1

    index = 0

    for inwin in hybla:
        generate_trace(inwin,names[index],fig_hybla)
        index += 1

    fig_cubic.update_layout(title="Cubic", xaxis_title="Time (s)", yaxis_title="Throughput (Mb/s)")
    fig_cubic.show()

    fig_bbr.update_layout(title="BBR", xaxis_title="Time (s)", yaxis_title="Throughput (Mb/s)")
    fig_bbr.show()

    fig_hybla.update_layout(title="Hybla", xaxis_title="Time (s)", yaxis_title="Throughput (Mb/s)")
    fig_hybla.show()
    
