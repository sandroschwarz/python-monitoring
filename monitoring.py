#!/bin/env python3

# Written by Sandro Schwarz

import threading as t # import threading to run monitoring idependently
import alarm as a # import own module (./alarm.py)
import psutil as p # import psutil (pip install requirements.txt) to get hardware stats
import os, time, platform # import built-in modules
import argparse # for parsing flags like '-i'

# Set up config parser, mainly used to check for interactive mode
parser = argparse.ArgumentParser(description="Monitor system health and send emails in case of emergencies.")
parser.add_argument("-i", action="store_true", default=False, help="Interactive mode. Set for watching stats indefinitely.", dest="boolean_switch")
args = parser.parse_args()

# Define a function to clear the screen
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")  

maxPid = 500 # INI?

if __name__ == "__main__":
    while True:
        # Define which stats should be monitored and how to find out it's percentage
        monitorStats = {
        "CPU": p.cpu_percent(),
        "RAM": p.virtual_memory().percent,
        "Disk": p.disk_usage("/").percent,
        "PID": round(len(p.pids())/maxPid*100, 2) # converting amount of PIDs to percentage first
        }

        clear()
        for i,j in monitorStats.items():
            t.Thread(target=a.specStat(j,i)).start() # start a thread that calls the alarm.py function specStat with percentage and description
            
        if args.boolean_switch == False: exit(1) # exit program if interactive mode is not set

        time.sleep(1) # wait a second until next iteration

