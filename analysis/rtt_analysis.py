import csv
import plotly
import sys
import os
import math

def parse_csv(csv_file):
    data_points = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    start_time = None
    for row in csv_reader:
        if line_count == 0:
            pass
        else:
            if row[4] != "192.168.1.102" and len(row[9]) > 0:
                if start_time == None:
                    start_time = sum(x * float(t) for x, t in zip([3600, 60, 1], row[11][12:30].split(":")))
                    data_points.append([float(row[9]),0])
                else:
                    data_points.append([float(row[9]),sum(x * float(t) for x, t in zip([3600, 60, 1], row[11][12:30].split(":"))) - start_time])
        line_count += 1
    return data_points

def average_data(data_points, time_frame):
    time_frame_min = 0
    time_frame_max = time_frame
    avg_rtt_list = []
    seconds_list = []
    data_points_in_time_frame_list = []
    margin_of_error_list = []
    rtt_sum_in_frame = 0
    samples = 0
    index = 0
    while time_frame_max < data_points[-1][1] and index < len(data_points):
        if data_points[index][1] >= time_frame_min and data_points[index][1] < time_frame_max:
            rtt_sum_in_frame += data_points[index][0]
            data_points_in_time_frame_list.append(data_points[index][0])
            samples += 1
            index += 1
        else:
            if samples > 0:
                avg_rtt = 1000*rtt_sum_in_frame/samples #milliseconds
                avg_rtt_list.append(avg_rtt)
                margin_of_error_list.append(margin_of_error(data_points_in_time_frame_list,avg_rtt,samples))
                seconds_list.append(time_frame_min)
            time_frame_min = time_frame_max
            time_frame_max += time_frame
            rtt_sum_in_frame = 0
            samples = 0
            data_points_in_time_frame_list = []
    return [avg_rtt_list,seconds_list,margin_of_error_list]
    
def margin_of_error(data_list,average,n):
    sum_squares = 0
    for x in data_list:
        sum_squares += (x-average)**2
    return 1.960*(math.sqrt(sum_squares/(n-1)))/(math.sqrt(n))

def generate_trace(csv_files_to_average, label, figure, color):
    total_data_points = []
    data_points = []
    averaged_lists = []

    for x in csv_files_to_average:
        data_points = parse_csv(open(x))
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

    figure.add_trace(plotly.graph_objects.Scatter(
        x=x+x_rev,
        y=y_upper+y_lower,
        fill='toself',
        fillcolor=f'rgba({color},0.2)',
        line_color='rgba(255,255,255,0)',
        # showlegend=False,
        name=label,
    ))
    figure.add_trace(plotly.graph_objects.Scatter(
        x=x, y=y,
        name=label,
        line_color=f'rgb({color})'
    ))


time_frame = 1
colors = ['255,0,0','0,255,0','0,0,255','255,0,255','0,255,255','255,255,0','0,128,255']

WIN_DIR_BBR = [3,5,10,20,40]
WIN_DIR = [3,5,10,20,40,100,250]
PCC_DIR = [180000,300000,600000,1200000,2400000]

if (sys.argv[1]=="across"):
    #analysis.py across <initcwnd> <trials>
    list_algorithms = ["cubic","bbr","hybla", "cubic_hystart_off"]
    letters = ["A","B","C","A"]
    initcwnd = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    figure = plotly.graph_objects.Figure()
    i = 0
    for algo in list_algorithms:
        paths = []
        for trial in range(num_trials):
            paths.append(os.path.join('initcwnd_data',f'{algo}',f'{initcwnd}',f'mlcnet{letters[i]}.cs.wpi.edu_{algo}_{trial}',f'mlcnet{letters[i]}.cs.wpi.edu.csv'))
        print(f"algorithm: {algo}")
        generate_trace(paths,algo,figure,colors[i])
        figure.update_layout(title=f"initcwnd {initcwnd}", xaxis_title="Time (s)", yaxis_title="Average RTT (ms)")
        i+=1
    figure.update_traces(mode='lines')
    figure.update_xaxes(range=[0,40])
    # figure.update_yaxes(range=[0,150])
    # figure.write_image(f"rtt_across_{initcwnd}.png")
    figure.show()
elif (len(sys.argv)==4):
    #analysis.py <algorithm> <letter> <trials>
    mlc_letter = sys.argv[2]
    num_trials = int(sys.argv[3])
    algorithm = sys.argv[1]
    if (algorithm =="pcc"):
        dirs = PCC_DIR
    elif (algorithm == "bbr"):
        dirs = WIN_DIR_BBR
    else:
        dirs = WIN_DIR
    i = 0
    figure = plotly.graph_objects.Figure()
    for inwin in dirs:
        paths = []
        for trial in range(num_trials):
            paths.append(os.path.join('initcwnd_data',f'{algorithm}',f'{inwin}',f'mlcnet{mlc_letter}.cs.wpi.edu_{algorithm}_{trial}',f'mlcnet{mlc_letter}.cs.wpi.edu.csv'))
        print(f"window: {inwin}")
        generate_trace(paths,inwin,figure,colors[i])
        figure.update_layout(title=algorithm, xaxis_title="Time (s)", yaxis_title="Average RTT (ms)")
        i+=1
    figure.update_traces(mode='lines')
    figure.update_xaxes(range=[0,40])
    # figure.update_yaxes(range=[0,150])
    # figure.write_image(f"rtt_{algorithm}.png")
    figure.show()   
else:
    mlc_letter = 'A'
    num_trials = 5
    algorithm = "cubic"
    dirs = WIN_DIR
    figure = plotly.graph_objects.Figure()
    inwin = '10'
    paths = []
    for trial in range(num_trials):
        paths.append(os.path.join('initcwnd_data',f'{algorithm}',f'{inwin}',f'mlcnet{mlc_letter}.cs.wpi.edu_{algorithm}_{trial}',f'mlcnet{mlc_letter}.cs.wpi.edu.csv'))
    print(f"window: {inwin}")
    generate_trace(paths,inwin,figure,colors[0])
    figure.update_layout(title=algorithm, xaxis_title="Time (s)", yaxis_title="Average RTT (ms)")     
    figure.update_traces(mode='lines')
    figure.update_xaxes(range=[0,40])
    # figure.update_yaxes(range=[0,150])
    # figure.write_image(f"rtt_{algorithm}.png")
    figure.show()  