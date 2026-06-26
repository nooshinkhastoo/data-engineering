#!/bin/bash

OUTPUT="report_connectivity.txt"

echo "===== Ping 8.8.8.8 =====" > $OUTPUT
ping -c 5 8.8.8.8 >> $OUTPUT

echo -e "\n===== Ping google.com =====" >> $OUTPUT
ping -c 5 google.com >> $OUTPUT

echo -e "\n===== DNS Resolution github.com =====" >> $OUTPUT
nslookup github.com >> $OUTPUT
