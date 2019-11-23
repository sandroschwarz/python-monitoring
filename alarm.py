#!/bin/env python3

# Written by Sandro Schwarz

import logging as l # used for logging to file
import socket as s # used to get machine FQDN (displayed in the logs)
import datetime as d # for getting and formatting out own date display
import smtplib as m # used for sending critical emails
import time as t # used for idling
import os as o # for checking if log folder exists and creating one in case it doesn't
import configparser as c # for loading config from config.ini

# initializing variables
lastMailSent = ""
lastLogEntry = ""

# CHECK FOR LOG FOLDER
if o.path.isdir("./logs") == False:
    o.mkdir("./logs")

# LOG CONFIG
LOG_FILENAME = d.datetime.now().strftime("%d-%m-%Y_%H-%M-%S.log") # Log will have a timestamp like this for its name
LOG_PATH = "./logs/{}".format(LOG_FILENAME)
LOG_FORMAT = "%(asctime)s %(fqdn)s %(message)s" # Defining how the log will be contructed
LOG_TEXT = "{desc} usage is: {percent}% ({status})" # Setting out custom log message text for reusing it later
LOG_DATEFORMAT = "%d.%m.%Y %H:%M:%S" # This will be our displayed timestamp in the log

# EMAIL CONFIG
config = c.ConfigParser()
config.read("config.ini")
port = config["EMAIL"]["port"]
smtpServer = config["EMAIL"]["smtpServer"]
messageHead = config["EMAIL"]["messageHead"]
messageBody = config["EMAIL"]["messageBody"]
fromAdd = config["EMAIL"]["fromAdd"]
toAdd = config["EMAIL"]["toAdd"]
message = "Subject: {}\n\n{}".format(messageHead, messageBody)


MACHINE_FQDN = s.getfqdn()
MAP = {"fqdn": MACHINE_FQDN} # used for formatting log lines

logCooldown = 1 # minute
mailCooldown = 1 #hour

# Basic log configuration, including log name, level of logging (set to DEBUG to get nominal stats as well)
l.basicConfig(
    format=LOG_FORMAT,
    datefmt=LOG_DATEFORMAT,
    filename=LOG_PATH,
    filemode="w+",
    level=l.WARNING,
)

def sendEmailWarning(spec, desc):
    with m.SMTP(smtpServer, port) as server:
        server.sendmail(fromAdd, toAdd, message.format(spec=spec, desc=desc, pc=s.getfqdn()))

# Main function for checking against soft and hard limits, logging accordingly and sending warnings
def specStat(spec, desc):
    global lastMailSent
    global lastLogEntry
    status = ""
    if 0 <= spec <= 80: # check if percentage is nominal
        status = "Nominal"
    elif 80 < spec < 90: # check if percentage is in soft limit
        status = "Warning"
        if lastLogEntry == "": # check if variable is empty, if empty, log and set variable accordingly
            l.warning(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now() # update lastLogEntry variable if 
        elif lastLogEntry + d.timedelta(minutes=logCooldown) < d.datetime.now(): # if last entry plus logCooldown is older than current time, then log
            l.warning(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
    else: # check if percentage is in hard limit (or even negative?)
        status = "Critical"
        if lastLogEntry == "":
            l.critical(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
        elif lastLogEntry + d.timedelta(minutes=logCooldown) < d.datetime.now():
            l.critical(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
        try:
            if lastMailSent == "":
                sendEmailWarning(spec, desc)
                lastMailSent = d.datetime.now()
            elif lastMailSent + d.timedelta(hours=mailCooldown) < d.datetime.now():
                sendEmailWarning(spec, desc)
                lastMailSent = d.datetime.now()
        except Exception as e:
            print("Couldn't send email:", e)
    output = LOG_TEXT.format(desc=desc, percent=spec, status=status)
    print(output)

if __name__ == "__main__":
    print("Sorry, this module is meant for importing only.")