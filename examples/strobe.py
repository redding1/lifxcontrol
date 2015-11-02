#!/usr/bin/env python
from lifxlan import *
import sys

def main():
    num_lights = 6
    lifx = LifxLAN(num_lights)

	lifxlan.set_color_all_lights(white, rapid=True)
    print("Toggling power of all lights...")
	while True:
		toggle_all_lights_power(lifx, 0.1)




def toggle_all_lights_power(lan, interval=0.5, num_cycles=3): #TEST
    lan.set_power_all_lights("off")
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        lan.set_power_all_lights("on", rapid)
        sleep(interval)
        lan.set_power_all_lights("off", rapid)
        sleep(interval)

def toggle_all_lights_color(lan, interval=0.5, num_cycles=3):
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        lan.set_color_all_lights(BLUE, rapid=rapid)
        sleep(interval)
        lan.set_color_all_lights(GREEN, rapid=rapid)
        sleep(interval)

if __name__=="__main__":
    main()
