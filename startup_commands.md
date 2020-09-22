## Glomma

- screen
- tcpdump
- ^a-d
- iperf3 -c mlcnet[a,b,c,d] -r
- screen -r
- ^c
- repeat 2-5

## mlc[a,b,c,d]

- screen
- iperf3 -s
- ^a-d
- tcpdump

ip route show

find default line

sudo ip route change [default line] initcwnd 10

ss -nli | grep cwnd
