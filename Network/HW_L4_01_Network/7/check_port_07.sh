#!/bin/bash

OUTPUT="check_port_report.txt"

echo "===== HTTP Port 80 =====" > $OUTPUT
telnet localhost 80 >> $OUTPUT 2>&1

echo -e "\n===== SSH Port 22 =====" >> $OUTPUT
telnet localhost 22 >> $OUTPUT 2>&1

echo -e "\n===== MySQL Port 3306 =====" >> $OUTPUT
telnet localhost 3306 >> $OUTPUT 2>&1

