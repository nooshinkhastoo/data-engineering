#!/bin/bash

OUTPUT="info_network.txt"

echo "===== Network Interfaces =====" > $OUTPUT
ip link show >> $OUTPUT

echo -e "\n===== Current IP Address =====" >> $OUTPUT
ip addr show >> $OUTPUT

echo -e "\n===== Default Gateway =====" >> $OUTPUT
ip route | grep default >> $OUTPUT

echo -e "\n===== DNS Servers =====" >> $OUTPUT
cat /etc/resolv.conf >> $OUTPUT
