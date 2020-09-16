import os,sys,subprocess

lines = []
with os.popen("tshark -r "+sys.argv[1]+" -T fields -e tcp.analysis.ack_rtt") as sharky:
    for line in sharky:
        lines.append(line)

lines = list(filter(None,lines))#remove whitespace
numbers = list(map(float,lines))#convert to float

print(sum(numbers)/len(numbers))#print result. can use numbers list to produce a plot though

'''
run this script to get average RTT

tshark -r <.pcap file name> -T fields -e tcp.analysis.ack_rtt

note: tshark is doing no filtering on non-ack packets so there is whitespace (hence the filter)
'''