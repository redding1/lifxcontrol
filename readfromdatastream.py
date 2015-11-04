#!/usr/bin/env python
#Script to test the ipscanning function within the main program.

#https://nodejs.org/dist/v4.2.2/node-v4.2.2-linux-armv6l.tar.gz
#sudo apt-get update
#sudo apt-get upgrade
#sudo apt-get install nodejs npm
#npm install -g phant

#http://phant.io/beaglebone/install/2014/07/03/beaglebone-black-install/#connecting-via-ssh


#curl -X GET 'https://data.sparkfun.com/input/YG0ARRlA3AIjDlyjVEyx?private_key=RbqpKKap1pTaMwkaoxkd&sensor1=3.71'

import nmap

scanip = '192.168.1.20'
connect_host = 0        
nm= nmap.PortScanner()

try:
    nm.scan(scanip,'22', '-n -sS -T5') #Fast scan
    #nm.scan(scanip,'80')# Slow Scan
    nm[scanip].state()
    print "Detected IP on network"
    connect_host = 1
except KeyError, e:
    connect_host = 0
    print "Did not detect IP on network"
