#!/usr/bin/python3
from datetime import date
from trial import Trial
import os
from command import run
from glob import glob
import time


DATA_DIR = './data/2020-10-06'


def tshark_command(pcap_file, output_file):
    return f"""
    nice tshark -r {pcap_file} \
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
        -e tcp.analysis.ack_rtt \
        -e ip.proto  \
        -e frame.time \
        -E header=y  \
        -E separator=,  \
        -E quote=d  \
        -E occurrence=f \
        > {output_file}
        """


def pcap_to_csv(pcap_file='./data/pcap.pcap'):
    """
    TODO this is optional
    """
    output_file = os.path.splitext(pcap_file)[0] + '.csv'

    command = tshark_command(pcap_file, output_file)
    run(command).wait()

    return output_file


def all_pcaps(data_dir=DATA_DIR):
    for dir in glob(f"{data_dir}/**/*"):
        if (not os.path.isdir(dir)):
            continue

        local = glob(f"{dir}/local.pcap")
        remote = [f for f in filter(lambda fname: not "local" in fname,
                                    glob(f"{dir}/*.pcap"))]
        remote = remote[0] if remote else None
        local = local[0] if local else None

        yield((local, remote, dir))


def all_trials_main():
    # roughly 1 day of trails
    machines = [
        #"mlcnetA.cs.wpi.edu",
        "mlcnetB.cs.wpi.edu"
        #"mlcnetC.cs.wpi.edu",
        # "mlcnetD.cs.wpi.edu"
    ]
    protocols = [
        #"cubic",
         "bbr"
        #"hybla",
        # "pcc"
    ]

    initcwnd = [
       # 3,
       # 5,
       #10,
       # 20,
       # 40,
       100,
       250
    ]

    dir = 'data/' + date.today().strftime("%Y-%m-%d")
    if not os.path.exists(dir):
        os.makedirs(dir)
    # roughly 24 hours

    for i in range(5):
        for j in initcwnd:
            for machine, protocol in zip(machines, protocols):
                print(machine, protocol)
                title = f"{dir}/{j}/{machine}_{protocol}_{i}"
    #            time.sleep(15)                
                trial = Trial(name=title, data="128MB", remote=machine)
                # trial.mock()
                trial.remote_tc(cc=protocol, initcwnd=j)
                trial.start()


def generate_pcaps():
    for local, remote, dir in all_pcaps():
        print(f"{local}, {remote}, {dir}")
        if local:
            pcap_to_csv(local)
        if remote:
            pcap_to_csv(remote)


if __name__ == "__main__":
    all_trials_main()
    generate_pcaps()
