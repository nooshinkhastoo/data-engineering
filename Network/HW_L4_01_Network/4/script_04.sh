#!/bin/bash

OUTPUT="port_status.txt"

echo "===== LISTEN Ports =====" > $OUTPUT
ss -tuln >> $OUTPUT

echo -e "\n===== ESTABLISHED Connections =====" >> $OUTPUT
ss -tan state established >> $OUTPUT

echo -e "\n===== Processes on Port 80 and 443 =====" >> $OUTPUT
sudo lsof -i :80 >> $OUTPUT
sudo lsof -i :443 >> $OUTPUT
