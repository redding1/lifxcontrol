#!/usr/bin/env python

#TODO
#Different states based on User IP -> Standard Mode, Party Mode

from lifxlan import *
import sys
import time
import signal
from copy import copy
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
    #thread.start_new_thread(pulse_device, (livingroom[0], 140, 0.3) )
    th = threading.Thread(target=pulse_device, args=(livingroom[0],60,0.5))
    th.start()
    print "Program End.."
    #pulse_device(livingroom[0], bpm=140, brightnesschange=0.3)

# Function Defs
def pulse_device(device, bpm=60, brightnesschange=0.5):
    half_period_s = 100.000
    half_period_s = bpm/60.000
    half_period_s = half_period_s*2
    half_period_s = 1/half_period_s
    half_period_ms = half_period_s*1000
    print "device is:"
    print(device)
    print "BPM is: %f" % bpm
    print "Wait Delay = %f" % half_period_ms
    original_color = device.get_color()
    dim_color = list(copy(original_color))
    dim_color[2] = int(dim_color[2]*brightnesschange)
    print "enter loop"
    last_beat = time.time()
    last_beat = last_beat-1447400000
    last_beat = last_beat*1000
    dimed = 0
    lit = 0
    while True:
        current_time = time.time()
        current_time = current_time - 1447400000
        current_time = current_time*1000
        if current_time > (last_beat + half_period_ms) and dimed == 0:
            device.set_color(dim_color, half_period_ms, rapid=True)
            dimed = 1
            print "Dim"
        if current_time > (last_beat + half_period_ms*2) and lit == 0:
            device.set_color(original_color, half_period_ms, rapid=True)
            lit = 1
            print "Lit"
        if current_time > last_beat + 2*half_period_ms:
            #New Beat Starting
            last_beat = time.time()
            last_beat = last_beat-1447400000
            last_beat = last_beat*1000
            dimed = 0
            lit = 0
            print "New Beat"
            print(last_beat)

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
