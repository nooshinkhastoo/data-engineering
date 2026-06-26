#!/bin/bash

echo "===== ROUTING TABLE =====" > analysis_routing.txt
ip route >> analysis_routing.txt

echo "" >> analysis_routing.txt
echo "===== TRACE ROUTE =====" >> analysis_routing.txt

traceroute 8.8.8.8 >> analysis_routing.txt

