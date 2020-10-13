import csv
import plotly
import sys
import os
import math

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
    data_points_in_time_frame_list = []
    margin_of_error_list = []
    mbits_in_frame = 0
    samples = 0
    index = 0
    while time_frame_max < data_points[-1][1] and index < len(data_points):
        if data_points[index][1] >= time_frame_min and data_points[index][1] < time_frame_max:
            mbits_in_frame += data_points[index][0]
            data_points_in_time_frame_list.append(data_points[index][0])
            samples += 1
            index += 1
        else:
            if samples > 0:
                avg_mbits = mbits_in_frame/samples
                avg_mbits_per_second = avg_mbits/time_frame
                avg_mbits_per_second_list.append(avg_mbits_per_second)
                margin_of_error_list.append(margin_of_error(data_points_in_time_frame_list,avg_mbits_per_second,samples))
            else:
                avg_mbits_per_second_list.append(0)
                margin_of_error_list.append(0)
            seconds_list.append(time_frame_min)
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            mbits_in_frame = 0
            samples = 0
            data_points_in_time_frame_list = []
    return [avg_mbits_per_second_list,seconds_list,margin_of_error_list]
    
def margin_of_error(data_list,average,n):
    if (n<=1):
        return 0
    sum_squares = 0
    for x in data_list:
        sum_squares += (x-average)**2
    return 1.960*(math.sqrt(sum_squares/(n-1)))/(math.sqrt(n))

def generate_trace(csv_files_to_average,time_frame):
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
    x = averaged_lists[1]
    x_rev = x[::-1]
    y = averaged_lists[0]
    y_upper = []
    y_lower = []
    for i in range(len(averaged_lists[2])):
        y_upper.append(averaged_lists[0][i] + averaged_lists[2][i])
        y_lower.append(averaged_lists[0][i] - averaged_lists[2][i])
    y_lower = y_lower[::-1]
    return [x,y,x+x_rev,y_upper+y_lower]

def run_throughput_analysis(files,time_frame=1):
    """Point of entry, only call this function

    Args:
        files (List[String]): List of file locations (trials from same data set, ex. cubic 10 or hybla 40)
        time_frame (int, optional): seconds between data points. Defaults to 1.

    Returns:
        List[List[float],List[float],List[float],List[float]]: List of four lists:
                                                                1. x values (times)
                                                                2. y values (throughput)
                                                                3. x values for margin of error
                                                                4. y values for margin of error
    """
    return generate_trace(files,time_frame)