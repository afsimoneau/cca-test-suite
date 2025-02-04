import csv
import plotly
import sys
import os
import math
from glob import glob

def parse_csv(csv_file):
    """Parses an individual CSV file into a set of data points

    Args:
        csv_file (File): a csv file

    Returns:
        List[List[int,int,float]]: A list of data points. 
                                   Each data points consist of 
                                   0: 1 if is a transmission, 
                                   1: 1 if is a retransmission, 
                                   2: time  in seconds
    """
    data_points = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    previous_bytes = 0
    start_time = None
    for row in csv_reader:
        if line_count == 0:
            pass
        else:
            if "130.215.28." in row[4]:
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
    """For a set of data points from a single CSV file, 
       calculate the average percent restransmissions per time frame

    Args:
        data_points (List[List[int,int,float]]): A list of data points. 
                                                 Each data points consist of 
                                                 0: 1 if is a transmission, 
                                                 1: 1 if is a retransmission, 
                                                 2: time  in seconds
        time_frame (float): increment of time in seconds in which new data points are calculated

    Returns:
        List[List[float,float]]: A list of data points containing the percent retransmissions, and the time in seconds
    """
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
            if transmissions_in_frame > 0:
                percent_retransmissions = 100*retransmissions_in_frame/transmissions_in_frame
            else:
                percent_retransmissions = 0
            percent_retransmissions_list.append([percent_retransmissions,time_frame_min])
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            transmissions_in_frame = 0
            retransmissions_in_frame = 0
    return percent_retransmissions_list

def average_data(data_points, time_frame):
    """Takes a list of data points from multiple CSV files (sorted by time) and 
       calculates both the average and margin of error across the multiple CSVs for each point

    Args:
        data_points (List[List[float,float]]): A list of data points containing the percent retransmissions, and the time in seconds
        time_frame (float): increment of time in seconds in which new data points are calculated

    Returns:
        List[List[float],List[float],List[float]]: A list containing three lists
                                                   0: list of average percentage of retransmissions within a time frame across multiple CSVs
                                                   1: a list of time intervals
                                                   2: list of margins of error across multiple CSVs for each time frame
    """
    time_frame_min = 0
    time_frame_max = time_frame
    avg_retransmission_list = []
    data_points_in_time_frame_list = [] #used to calculate margin of error
    seconds_list = []
    margin_of_error_list = []
    percent_sum_in_frame = 0
    samples = 0
    index = 0
    while time_frame_max < data_points[-1][1] and index < len(data_points):
        if data_points[index][1] >= time_frame_min and data_points[index][1] < time_frame_max:
            percent_sum_in_frame += data_points[index][0]
            data_points_in_time_frame_list.append(data_points[index][0])
            samples += 1
            index += 1
        else:
            if samples > 0:
                avg_percent = percent_sum_in_frame/samples
                avg_retransmission_list.append(avg_percent)
                margin_of_error_list.append(margin_of_error(data_points_in_time_frame_list,avg_percent,samples))
            else:
                avg_retransmission_list.append(0)
                margin_of_error_list.append(0)
            seconds_list.append(time_frame_min)
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            percent_sum_in_frame = 0
            samples = 0
    return [avg_retransmission_list,seconds_list,margin_of_error_list]

def margin_of_error(data_list,average,n):
    if (n<=1):
        return 0
    sum_squares = 0
    for x in data_list:
        sum_squares += (x-average)**2
    return 1.960*(math.sqrt(sum_squares/(n-1)))/(math.sqrt(n))

def generate_trace(csv_files_to_average, time_frame):
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

def run_retransmission_analysis(files,time_frame=1):
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