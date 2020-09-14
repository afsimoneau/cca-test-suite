with open("rtt.txt") as f:
    lines = list(filter(None,f.read().splitlines()))
    numbers = list(map(float,lines))

print(sum(numbers)/len(numbers))
print((16558.13 * 6996)/1000000)

'''
heres the tshark command used to create rtt.txt:

tshark -r testcap.pcap -T fields -e tcp.analysis.ack_rtt > rtt.txt

note: tshark is doing no filtering on non-ack packets so there is whitespace (hence the filter on line 2)
'''