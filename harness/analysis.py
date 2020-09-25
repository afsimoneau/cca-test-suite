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

def average_data(data_points):
    time_frame_min = 0
    time_frame_max = 0.1
    avg_bytes_list = []
    seconds_list = []
    bytes_in_frame = 0
    samples = 0
    index = 0
    while time_frame_max < data_points[-1][1] and index < len(data_points):
        if data_points[index][1] >= time_frame_min and data_points[index][1] < time_frame_max:
            bytes_in_frame += data_points[index][0]
            samples += 1
            index += 1
        else:
            try:
                avg_bytes = bytes_in_frame/samples
                avg_megabits = 8*avg_bytes/1000000
                avg_bytes_list.append(avg_megabits)
            except ZeroDivisionError:
                avg_bytes_list.append(0)
            seconds_list.append(time_frame_min)
            time_frame_min = time_frame_max
            time_frame_max += 0.1
            bytes_in_frame = 0
            samples = 0
    return [avg_bytes_list,seconds_list]
    

def plot(bytes_list, time_list):
    fig = plotly.graph_objects.Figure(data=plotly.graph_objects.Scatter(x=time_list,y=bytes_list), x="Time (s)", y="Throughput (Mb)")
    fig.show()

cubic_10 = [".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_0\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_1\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_2\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_3\\local.csv",\
            ".\\initcwnd_data\\cubic\\10\\mlcnetA.cs.wpi.edu_cubic_4\\local.csv"]

total_data_points = []
for x in cubic_10:
    data_points = parse_csv(open(x))
    for y in data_points:
        total_data_points.append(y)

total_data_points = sorted(total_data_points,key=lambda x: x[1])
averaged_lists = average_data(total_data_points)
plot(averaged_lists[0],averaged_lists[1])