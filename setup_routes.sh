#!/bin/bash

#
# Hard-code routes from glomma to the "MLC" servers
# to go via the satellite link.
#
# Run with: sudo ./setup_routes.sh
#
# Version 2
#

for host in "mlcnetA.cs.wpi.edu" "mlcnetB.cs.wpi.edu" "mlcnetC.cs.wpi.edu" "mlcnetD.cs.wpi.edu"
do
    sudo ip route add `dig +short $host` via 192.168.1.1 dev eno2
    sudo ip route show match `dig +short $host`
done

sudo ip route add 192.168.100.0/24 dev eno2
