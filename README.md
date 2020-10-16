# cca-test-suite

Test suite and scripts for WPI students working on the ISU "CCA over a satellite"

Usage notes: This is to simplify the distribution, so mainly using master is fine unless you want to edit/improve a script that is already established

## Running Experiments

There are five servers we use to run experiments "glomma.cs.wpi.edu" and mlcnet{a,b,c,d}.cs.wpi.edu. The mlcnet servers are where the congestion control algorithms are changed. All tests have to be started on glomma to ensure that the connection goes through the satellite connection. If glomma is ever restarted the setup_routes.sh script must be run to setup the proper ip routing tables. Most of the code in this folder was from Saahil Claypool's [repo](https://github.com/SaahilClaypool/Satellite)

Inside of the data_collection folder there are three scripts that we used to run experiments.

-   all_trials.py: This script is used to run the tests and then convert collected pcap files into csvs.
-   trial.py: Code for each individual test
-   get_cwnd.sh: This script has to be copied to your home folder on mlcnet{a,b,c,d}.cs.wpi.edu. It is used to collect the cwnd during the tests.

## Analysis

We currently evaluate tests based on cwnd size, throughput, rtt, retransmission, and time to steady state.

Inside of the analysis folder we have all the scripts we used for analysis.

-   all_analysis.py: Use this script to generate plotly graphs of experiments. This script can definitely be improved.
    -   In order to generate a graph the data must be stored in the folder final data.
    -   If you add a new data folder you must add its name to the algosToPlot list in main() and algos list in getDirs()
    -   This script generates pickle files of the analysis objects to prevent the script from having to run the analysis everytime it runs. If you change the data you must change reload to True. New folders will always be analyzed.
-   cwnd_analysis.py: Analyses cwnd data
    -   dir = path to initcwnd folder in each folder. ex "final_data/brr/10"
    -   cwnd_analysis.getAverage(dir)
    -   returns pandas dataframe
-   retransmission_analysis.py: Retransmission analysis
    -   localPaths = list of paths to local csvs in a folder like initcwnd folder
    -   retransmission_analysis.run_throughput_analysis(localPaths)
    -   Check function comments for return value info
-   rtt_analysis.py: RTT analysis

    -   localPaths = list of paths to local csvs in a folder like initcwnd folder
    -   rtt_analysis.run_throughput_analysis(localPaths)
    -   Check function comments for return value info

-   throughput_analysis.py: Throuput analysis
    -   localPaths = list of paths to local csvs in a folder like initcwnd folder
    -   throughput_analysis.run_throughput_analysis(localPaths)
    -   Check function comments for return value info

## Tools to use:

UDPing
iperf3
tcpdump
use -s for snaplen
use -w for write (need file name)
use -i for interface (eno2)

screen (to pop out tcpdump into its own terminal)
tshark
sysctl
