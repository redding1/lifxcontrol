#!/usr/bin/env python


import nmap


global Matt_Home
global Matt_Home_TimeOut
global connect_host

Matts_iPhone_IP = '192.168.1.20'
Matt_Home = True
Matt_Home_TimeOut = 0
connect_host = 0
nm = 0
         
nm= nmap.PortScanner()
try:
    #nm.scan(Matts_iPhone_IP,'80', '-n -sS -T5')
    nm.scan(Matts_iPhone_IP,'80')
    nm[Matts_iPhone_IP].state()
    print "found IP"
    connect_host = 1
except KeyError, e:
    connect_host = 0
    print "didn't find IP"

##if connect_host == 1:
##    print "Matt in network"
##    Matt_Home_TimeOut = 0
##    if Matt_Home == False:
##        Matt_Home = True
##        print "Welcome Home Matt!"
##else:
##    print "matt not in network"
##    if Matt_Home_TimeOut > 200:
##        print "timeout over 200"
##        if Matt_Home == True:
##            Matt_Home = False
##            print "Goodbye Matt!"
##    else:
##        Matt_Home_TimeOut += 1
##        print "Matt Timeout: %i" % Matt_Home_TimeOut  

