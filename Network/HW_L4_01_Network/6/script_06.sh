#!/bin/bash

OUTPUT="report_performance.txt"

echo "===== Bandwidth Test =====" > $OUTPUT
iperf3 -c SERVER_IP >> $OUTPUT

echo -e "\n===== Latency Test =====" >> $OUTPUT
ping -c 10 google.com >> $OUTPUT

echo -e "\n===== Jitter Test =====" >> $OUTPUT
ping -i 0.2 -c 20 google.com >> $OUTPUT

echo -e "\n===== Packet Loss =====" >> $OUTPUT
ping -c 20 8.8.8.8 >> $OUTPUT

#نصب iperf3:
#sudo apt install iperf3
#سرور:
#iperf3 -s
#کلاینت:
#iperf3 -c SERVER_IP
