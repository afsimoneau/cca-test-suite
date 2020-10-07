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

WIN_DIR_BBR = [3,5,10,20,40]
WIN_DIR = [3,5,10,20,40,100,250]
PCC_DIR = [180000,300000,600000,1200000,2400000]

if (len(sys.argv)==4):
    #retransmission_average.py <algorithm> <letter> <trials>
    num_trials = int(sys.argv[3])
    mlc_letter = sys.argv[2]
    algorithm = sys.argv[1]
    if (algorithm =="pcc"):
        dirs = PCC_DIR
    elif (algorithm == "bbr"):
        dirs = WIN_DIR_BBR
    else:
        dirs = WIN_DIR
    
    figure = plotly.graph_objects.Figure()
    for inwin in dirs:
        paths = []
        for trial in range(num_trials):
            paths.append(f"./../initcwnd_data/{algorithm}/{inwin}/mlcnet{mlc_letter}.cs.wpi.edu_{algorithm}_{trial}/local.csv")
        print(f"window: {inwin}")
        generate_trace(paths,inwin,figure)

    figure.update_layout(title=f"{algorithm} {inwin}", xaxis_title="Time (s)", yaxis_title="Retransmission Rate")
    figure.update_xaxes(range=[0,40])
    figure.update_yaxes(range=[0,100])
    figure.write_image(f"average_retransmission_{algorithm}.png")
    figure.show()