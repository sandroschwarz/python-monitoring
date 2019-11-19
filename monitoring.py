#!/bin/env python

import threading as t # import threading to run monitoring idependently
import alarm as a # import own module (./alarm.py)
import psutil as p # import psutil (pip install requirements.txt) to get hardware stats
import os, time, platform # import built-in modules

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")  

maxPid = 500 # INI?

while True:
    monitorStats = {
    "CPU": p.cpu_percent(),
    "RAM": p.virtual_memory().percent,
    "Disk": p.disk_usage("/").percent,
    "PID": round(len(p.pids())/maxPid*100, 2) # converting amount of PIDs to percentage first
    }

    clear()
    for i,j in monitorStats.items():
        t.Thread(target=a.specStat(j,i)).start()
        
    time.sleep(.1)

