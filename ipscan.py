#!/usr/bin/env python
#Script to test the ipscanning function within the main program.

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
