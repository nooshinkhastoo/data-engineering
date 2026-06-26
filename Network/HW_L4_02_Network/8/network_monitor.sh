#!/bin/bash

LOG="monitoring_log.txt"

while true
do
    echo "=========================" >> $LOG
    date >> $LOG

    echo "" >> $LOG
    echo "NETWORK INTERFACES" >> $LOG
    ip -s link >> $LOG

    echo "" >> $LOG
    echo "ACTIVE CONNECTIONS" >> $LOG
    netstat -tun | wc -l >> $LOG

    echo "" >> $LOG
    echo "TOP IP TRAFFIC" >> $LOG
    netstat -tun | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head -5 >> $LOG

    sleep 5
done

