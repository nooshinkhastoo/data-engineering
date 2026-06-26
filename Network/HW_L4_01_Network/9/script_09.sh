#!/bin/bash

sudo ufw --force enable

sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow from 192.168.1.0/24 to any port 22
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

sudo ufw status verbose > firewall_rules.txt

