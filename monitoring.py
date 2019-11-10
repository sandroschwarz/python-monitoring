import alarm # import own module (./alarm.py)
import os, time # import built-in modules
import psutil as p # import psutil (pip install psutil)

def clear():
    os.system("cls")

maxPid = 500

while True:
    cpuPerc = p.cpu_percent()
    virtMem = p.virtual_memory().percent
    diskUsage = p.disk_usage("C:").percent
    pidCount = len(p.pids())
    clear()
    alarm.specStat(cpuPerc, "CPU")
    alarm.specStat(virtMem, "RAM")
    alarm.specStat(diskUsage, "Disk")
    alarm.specStat(round(pidCount/maxPid*100, 2), "PID")
    time.sleep(1)

