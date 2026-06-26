#!/bin/bash

REPORT="https_test_report.txt"

echo "HTTPS TEST REPORT" > $REPORT
echo "======================" >> $REPORT

echo "" >> $REPORT
echo "1. CURL REQUEST" >> $REPORT
curl -I https://google.com >> $REPORT 2>&1

echo "" >> $REPORT
echo "2. SSL CERTIFICATE CHAIN" >> $REPORT
echo | openssl s_client -connect google.com:443 -servername google.com 2>/dev/null | openssl x509 -noout -issuer -subject >> $REPORT

echo "" >> $REPORT
echo "3. TLS VERSION" >> $REPORT
echo | openssl s_client -connect google.com:443 2>/dev/null | grep "Protocol" >> $REPORT

echo "" >> $REPORT
echo "4. CERTIFICATE EXPIRATION DATE" >> $REPORT
echo | openssl s_client -connect google.com:443 -servername google.com 2>/dev/null | openssl x509 -noout -dates >> $REPORT

echo "" >> $REPORT
echo "Report generated successfully."

