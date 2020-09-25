import csv
import plotly

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
            if row[4] == "130.215.28.202":
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
    
def generate_trace(csv_files_to_average, label):
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

    fig.add_trace(plotly.graph_objects.Scatter(
        x=averaged_lists[1],
        y=averaged_lists[0],
        name=label  
    ))

time_frame = 1
fig = plotly.graph_objects.Figure()

cubic_10 = [".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]
cubic_20 = [".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
            ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
            ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
            ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
            ".\\initcwnd_data\\cubic\\20\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]
cubic_40 = [".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
            ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
            ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
            ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
            ".\\initcwnd_data\\cubic\\40\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]
cubic_5  = [".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
            ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
            ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
            ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
            ".\\initcwnd_data\\cubic\\5\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]
cubic_3  = [".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
            ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
            ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
            ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
            ".\\initcwnd_data\\cubic\\3\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]

all_cubic = [cubic_3,cubic_5,cubic_10,cubic_20,cubic_40]
names = ["3","5","10","20","40" ]
index = 0

for inwin in all_cubic:
    generate_trace(inwin,names[index])
    index += 1

fig.update_layout(title="Cubic", xaxis_title="Time (s)", yaxis_title="Throughput (Mb/s)")
fig.show()