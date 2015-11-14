#!/usr/bin/env python

#TODO
#Different states based on User IP -> Standard Mode, Party Mode

from lifxlan import *
import sys
import time
import signal
from copy import copy
import curses
import threading

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
    num_lights = 6 #Num Lights to control

    # Variables
    global livingroom
    global bedroom
    global bpm
    global brightnesschange
     
    livingroom = []
    bedroom = []




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
        if "Bedroom" in allLights[i].get_label():
            bedroom.append(allLights[i])
            print "Added %s to Bed Room Group" % allLights[i].get_label()
    NumLivingLights = len(livingroom)
    NumBedroomLights = len(bedroom)
    
    # Main Program
    print "Program Starting..."
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.addstr(0,10,"Hit 'q' to quit")
    stdscr.refresh()
    key = ''


    bpm = 80
    brightnesschange = 0.6

    
    half_period_s = 100.000
    half_period_s = bpm/60.000
    half_period_s = half_period_s*2
    half_period_s = 1/half_period_s
    half_period_ms = half_period_s*1000
    original_color = livingroom[0].get_color()
    dim_color = list(copy(original_color))
    dim_color[2] = int(dim_color[2]*brightnesschange)

    while key != ord('q'):
        key = stdscr.getch()
        stdscr.addch(20,25,key)
        stdscr.refresh()
        if key == curses.KEY_UP: 
            stdscr.addstr(2, 20, "Up")
            pulse_device_once(livingroom[0], half_period_ms, dim_colour, original_color)
        elif key == curses.KEY_DOWN: 
            stdscr.addstr(3, 20, "Down")
            pulse_device_once(livingroom[1], half_period_ms=200, dim_colour, original_color)
    curses.endwin()

def pulse_device_once(device, half_period_ms=200, dim_colour, original_color):
    device.set_color(dim_color, half_period_ms, rapid=True)
    sleep(half_period_ms/1000)
    device.set_color(original_color, half_period_ms, rapid=True)

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
      
if __name__=="__main__":
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    main()
