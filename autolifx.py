#!/usr/bin/env python

#TODO
#Different states based on User IP -> Standard Mode, Party Mode

from lifxlan import *
import sys
from datetime import datetime
#from time import sleep
import time
import nmap
import signal


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

def main():
    # User Inputs
    User_IP = '192.168.1.20'
    num_lights = 6 #Num Lights to control
    TimeOut_Limit = 200
    
    # Variables
    global User_Home
    global User_IP_TimeOut
    global connect_host
    global livingroom
    global bedroom
    global networkinfo
    
    livingroom = []
    bedroom = []
    User_Home = True
    AutoOnOff = True
    User_IP_TimeOut = 0
    connect_host = 0
    networkinfo = nmap.PortScanner()

    # Inital Setup
    print("Discovering lights...")
    lifx = LifxLAN(num_lights)
    allLights = lifx.get_lights() # get allLights
    print("\nFound {} light(s)".format(len(allLights)))
    #for d in allLights:
        #print(d)

    # Group Lights
    # Example: All lights in Living room, change lifx bulb label to "Living something"
    # - allDevices = All Lights
    # - livingroom = Living Room
    # - bedroom = Bed Room
    for i in range(0,num_lights):
        if "Living" in allLights[i].get_label():       
            livingroom.append(allLights[i])
            print "Added %s to Living Group" % allLights[i].get_label()
        if "Reds" in allLights[i].get_label(): # Change "Reds" to "Bed" if your lights are "Bed 1" Bed2" etc
            bedroom.append(allLights[i])
            print "Added %s to Bed Room Group" % allLights[i].get_label()
    NumLivingLights = len(livingroom)
    NumBedroomLights = len(bedroom)
    
    # Main Program
    while True:
        sleep(1)
        time = datetime.now().time()
        nm = 0

        # **** Timed on/off ****#
        # Lights On
        print "Current time: %s" % time.hour
        print "Current time: %s" % time.minute
        if (time.hour == 16 and time.minute == 10):
            if AutoOnOff == False:
                lifxlan.set_power_all_lights("on", rapid=True) #TODO: Try lifxlan.set_power_all_lights("on", 5, rapid=True) 
                sleep(0.1)
                lifxlan.set_color_all_lights("warm_white", rapid=True)
                AutoOnOff = True
                print "Turning Lights on %s" % time
        # Lights Off
        if(time.hour == 22 and time.minute == 52):
            if AutoOnOff == True:
                lifxlan.set_power_all_lights("off", rapid=True)
                AutoOnOff = False
                print "Turning Lights off %s" % time

        # **** Detect IP Leaving House ****#
        connect_host = port_scan(User_IP)
        if connect_host == 1:
            print "IP %s Found in network" % User_IP
            User_IP_TimeOut = 0
            if User_Home == False:
                User_Home = True
                print "Welcome Home!"
        else:
            print "Connection lost with %s" % User_IP
            if User_IP_TimeOut > TimeOut_Limit:
                print "Timeout has exceeded %i cycles." % TimeOut_Limit
                if User_Home == True:
                    User_Home = False
                    print "Goodbye!"
            else:
                User_IP_TimeOut += 1
                print "User IP Timeout count: %i" % User_IP_TimeOut

# Function Defs
def port_scan(ip):
    try:
        networkinfo.scan(ip,'22', '-n -sS -T5')
        networkinfo[ip].state()
        print "IP Active: %s" % ip
        connect_host = 1
    except KeyError, e:
        connect_host = 0
        print "IP Inactive: %s" % ip
    return connect_host    

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)
      
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
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    main()
