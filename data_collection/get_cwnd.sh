#!/bin/bash

# run this script using watch, which can be used to run the command on a set time interval
# the output used can create a csv
# example: watch -n 0.1 "./get_cwnd.sh >> cwnd.csv"

# run away this is scary

if [ ! -f ./cwnd.csv ]; then
    echo "time,cwnd" > cwnd.csv
fi

ss -i |  awk '/5201/ {if ($4 != 0) getline; if ($10 != "") print $10}' |  sed 's/^.*://' | sed -e "s/^/$(date "+%Y-%m-%d %H:%M:%S.%6N"),/"

# >>> ss -i
### gets socket info

# >>> awk '/5201/ {if ($4 != 0) getline; if ($10 != "") print $10}'
### gets the flows that use port 5201 which is the port used for iperf

### there's two flows using port 5201 and one is used send the iperf payload so we parse our the flow that has a non zero packets sent
### ^^^ thats {if ($4 != 0)

### then we get the next line which contains all the important info
### in the second if statement we check if the 10th word exists because for the first line that contains the port info is also pasted to this if statement

# >>> sed 's/^.*://'
### this parses "cwnd:10" => "10"

# >>> sed -e "s/^/$(date "+%Y-%m-%d %H:%M:%S.%6N"),/"
### this adds a timestamp to the output which looks like: "2020-10-06 22:27:32.144418,100"