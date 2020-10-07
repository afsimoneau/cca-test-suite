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

WIN_DIR_BBR = [3,5,10,20,40]
WIN_DIR = [3,5,10,20,40,100,250]
PCC_DIR = [180000,300000,600000,1200000,2400000]

if (sys.argv[1]=="across"):
    #analysis.py across <initcwnd> <trials>
    list_algorithms = ["cubic","bbr","hybla", "cubic_hystart_off"]
    letters = ["A","B","C"]
    initcwnd = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    figure = plotly.graph_objects.Figure()
    i = 0
    for algo in list_algorithms:
        paths = []
        for trial in range(num_trials):
            paths.append(f"./../initcwnd_data/{algo}/{initcwnd}/mlcnet{letters[i]}.cs.wpi.edu_{algo}_{trial}/local.csv")
        print(f"algorithm: {algo}")
        generate_trace(paths,algo,figure)
        figure.update_layout(title=f"initcwnd {initcwnd}", xaxis_title="Time (s)", yaxis_title="Throughput (Mb/s)")
        i+=1
    figure.show()
elif (len(sys.argv)==4):
    #analysis.py <algorithm> <letter> <trials>
    num_trials = int(sys.argv[3])
    mlc_letter = sys.argv[2]
    algorithm = sys.argv[1]
    figure = plotly.graph_objects.Figure()
    if (algorithm =="pcc"):
        dirs = PCC_DIR
    elif (algorithm == "bbr"):
        dirs = WIN_DIR_BBR
    else:
        dirs = WIN_DIR
    
    for inwin in dirs:
        paths = []
        for trial in range(num_trials):
            paths.append(f"./../initcwnd_data/{algorithm}/{inwin}/mlcnet{mlc_letter}.cs.wpi.edu_{algorithm}_{trial}/local.csv")
        print(f"window: {inwin}")
        generate_trace(paths,inwin,figure)
        figure.update_layout(title=algorithm, xaxis_title="Time (s)", yaxis_title="Throughput (Mb/s)")
    figure.show()   