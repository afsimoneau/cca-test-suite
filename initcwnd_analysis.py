import progressbar as progress
import subprocess as sub
from glob import glob
import csv

CCA_DIRS = [
    './initcwnd_data/cubic',
    './initcwnd_data/bbr',
    './initcwnd_data/hybla'
    ]

WIN_DIR = [
    '/3',
    '/5',
    '/10',
    '/20',
    '/40'
    ]

RUN_DIRS = {
    CCA_DIRS[0]:'/mlcnetA.cs.wpi.edu_cubic_',
    CCA_DIRS[1]:'/mlcnetB.cs.wpi.edu_bbr_',
    CCA_DIRS[2]:'/mlcnetC.cs.wpi.edu_hybla_'
}

NUM_RUN = 5

RERUN = False


def tshark_command(pcap_file, output_file):
    return f"""nice tshark -r {pcap_file} \
        -T fields  \
        -e frame.number  \
        -e frame.time_epoch  \
        -e eth.src  \
        -e eth.dst  \
        -e ip.src  \
        -e ip.dst  \
        -e tcp.srcport \
        -e tcp.dstport \
        -e tcp.seq \
        -e tcp.analysis.bytes_in_flight \
        -e tcp.analysis.ack_rtt \
        -e ip.proto  \
        -e frame.time \
        -E header=y  \
        -E separator=,  \
        -E quote=d  \
        -E occurrence=f \
        > {output_file}"""

def process():
    for cca in CCA_DIRS:
        for win in WIN_DIR:
            if (RERUN==True):
                #if we need to reprocess the data CSV's
                for i in range(NUM_RUN):
                    directory = cca+win+RUN_DIRS.get(cca)+str(i)#directory for path to file
                    print(directory)
                    sub.run(tshark_command(directory+"/local.pcap",directory+"/rerun-local.csv"),shell=True)
            
            for i in range(NUM_RUN):
                source = open(cca+win+RUN_DIRS.get(cca)+str(i)+'/rerun-local.csv',mode='r')
                csv_reader = csv.reader(source, delimiter=',')
                dict
                for row in csv_reader:
                    if row[6]==5201:
                        #port is from server, this is a downlink packet



            combine_csv = csv.writer(open(cca+win+'/combine.csv',mode='w',delimiter=','))
            
            
                            


    return

if __name__ == "__main__":
    process()