import os,sys,subprocess,re

lines = []
with os.popen("tshark -r "+sys.argv[1]+" -T fields -e tcp.analysis.ack_rtt") as sharky:
    for line in sharky:
        lines.append(line)

cleanList = []
for dirty in lines:
    temp = re.sub("[^\d.]","",dirty)
    if temp!="":
        cleanList.append(temp)#filtering
numbers = list(map(float,cleanList))#convert to float

print(sum(numbers)/len(numbers))#print result. can use numbers list to produce a plot though

'''
run this script to get RTT

tshark -r <.pcap file name> -T fields -e tcp.analysis.ack_rtt
'''