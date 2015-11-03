#!/usr/bin/env python

#TODO
#
#Different states based on MattsIphone IP -> Standard Mode, Party Mode

from lifxlan import *
import sys
from datetime import datetime
from time import sleep

from netaddr import IPNetwork, IPAddress
import socket,struct
import nmap
colors = {
    "red": RED, 
    "orange": ORANGE, 
    "yellow": YELLOW, 
    "green": GREEN, 
    "cyan": CYAN, 
    "blue": BLUE, 
    "purple": PURPLE, 
    "pink": PINK, 
    "white": WHITE, 
    "cold_white": COLD_WHTE, 
    "warm_white": WARM_WHITE, 
    "gold": GOLD
}


#network = "192.168.1.0/24"
#address = dottedQuadToNum("192.168.1.20")
#networkb = networkMask("192.168.0.0",24)



def main():

    global Matt_Home
    global Matt_Home_TimeOut
    global connect_host
    
    address = dottedQuadToNum("192.168.1.20")
    networkb = networkMask("192.168.1.0",24)
    Matts_iPhone_IP = "192.168.1.20"
    Matt_Home = True
    Matt_Home_TimeOut = 0
    connect_host = 0
    nm = 0
    
    num_lights = 6 #Num Lights to control
    print("Discovering lights...")
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights() # get devices
    print("\nFound {} light(s):\n".format(len(devices)))
    #for d in devices:
        #print(d)

    while True:
        sleep(1)
        time = datetime.now().time()

        #Turn On lights @ 4:00pm
        if (time.hour == 16 and time.minute == 10):
            if AutoOnOff == False:
                lifxlan.set_power_all_lights("on", rapid=True) #TODO: Try lifxlan.set_power_all_lights("on", 5, rapid=True) 
                sleep(0.2)
                lifxlan.set_color_all_lights("warm_white", rapid=True)
                AutoOnOff = True
                print "Another Day ANOTHER LIGHT! 410 on"
                
        #Turn Off Lights @ 1230am
        if(time.hour == 0 and time.minute == 30):
            if AutoOnOff == True:
                lifxlan.set_power_all_lights("off", rapid=True)
                AutoOnOff = False
                "Sweet Dreams. 1230 night time"

        #Detect IP Leaving House
        #print addressInNetwork(address,networkb)        
        nm= nmap.PortScanner()
        try:
            #nm.scan(Matts_iPhone_IP,'80', '-n -sS -T5')
            nm.scan(Matts_iPhone_IP,'80')
            #nm[Matts_Iphone_IP].state()
            print "found IP"
            connect_host = 1
        except KeyError, e:
            connect_host = 0
            print "didn't find IP"

        if connect_host == 1:
            print "Matt in network"
            Matt_Home_TimeOut = 0
            if Matt_Home == False:
                Matt_Home = True
                print "Welcome Home Matt!"
        else:
            print "matt not in network"
            if Matt_Home_TimeOut > 200:
                print "timeout over 200"
                if Matt_Home == True:
                    Matt_Home = False
                    print "Goodbye Matt!"
            else:
                Matt_Home_TimeOut += 1
                print "Matt Timeout: %i" % Matt_Home_TimeOut  


#for i in range(0:num_lights-1):
#if "Living" in devices[i].get_label()       
#living.append(devices[i])



def makeMask(n):
    "return a mask of n bits as a long integer"
    return (2L<<n-1) - 1

def dottedQuadToNum(ip):
    "convert decimal dotted quad string to long integer"
    return struct.unpack('L',socket.inet_aton(ip))[0]

def networkMask(ip,bits):
    "Convert a network address to a long integer" 
    return dottedQuadToNum(ip) & makeMask(bits)

def addressInNetwork(ip,net):
   "Is an address in a network"
   return ip & net == net
       
def toggle_device_power(device, interval=0.5, num_cycles=3): #TEST
    original_power_state = device.get_power()
    device.set_power("off")
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        device.set_power("on", rapid)
        sleep(interval)
        device.set_power("off", rapid)
        sleep(interval)
    device.set_power(original_power_state)

def toggle_light_color(light, interval=0.5, num_cycles=3):
    original_color = light.get_color()
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        light.set_color(BLUE, rapid=rapid)
        sleep(interval)
        light.set_color(GREEN, rapid=rapid)
        sleep(interval)
    light.set_color(original_color)

if __name__=="__main__":
    main()
