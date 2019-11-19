import logging as l # used for logging to file
import socket as s # used to get machine FQDN (displayed in the logs)
import datetime as d # for getting and formatting out own date display
import smtplib as m # used for sending critical emails
import time as t # used for waiting

# initializing variables
lastMailSent = ""
lastLogEntry = ""

# LOG CONFIG
LOG_FILENAME = d.datetime.now().strftime("%d-%m-%Y_%H-%M-%S.log") # Log will have a timestamp like this for its name
LOG_PATH = "./logs/{}".format(LOG_FILENAME)
LOG_FORMAT = "%(asctime)s %(fqdn)s %(message)s" # Defining how the log will be contructed
LOG_TEXT = "{desc} usage is: {percent}% ({status})" # Setting out custom log message text for reusing it later
LOG_DATEFORMAT = "%d.%m.%Y %H:%M:%S" # This will be our displayed timestamp in the log

# EMAIL CONFIG
port = 1025  # For running a local SMTP server on port 1025
smtpServer = "localhost"
message = "Subject: [CRITICAL] Hard Limit Warning!\n\nWarning, {desc} is at {spec}% and therefore over the hard limit of 90%."
fromAdd = "alarm@localhost"
toAdd = "admin@localhost"

MACHINE_FQDN = s.getfqdn()
MAP = {"fqdn": MACHINE_FQDN} # used for formatting log lines



# Basic log configuration, including log name, level of logging (set to DEBUG to get nominal stats as well)
l.basicConfig(
    format=LOG_FORMAT,
    datefmt=LOG_DATEFORMAT,
    filename=LOG_PATH,
    filemode='w',
    level=l.WARNING,
)

def sendEmailWarning(spec, desc):
    with m.SMTP(smtpServer, port) as server:
        server.sendmail(fromAdd, toAdd, message.format(spec=spec, desc=desc))

# Main function for checking against soft and hard limits, logging accordingly and sending warnings
def specStat(spec, desc):
    global lastMailSent
    global lastLogEntry
    status = ""
    if 0 <= spec <= 80: 
        status = "Nominal"
        if lastLogEntry == "":
            print("Date of last log entry not found, writing one now and setting the var.")
            l.info(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
        elif lastLogEntry + d.timedelta(hours=12) < d.datetime.now():
            l.info(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
    elif 80 < spec < 90:
        status = "Warning"
        if lastLogEntry == "":
            print("Date of last log entry not found, writing one now and setting the var.")
            l.warning(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
        elif lastLogEntry + d.timedelta(hours=12) < d.datetime.now():
            l.warning(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
    else:
        status = "Critical"
        if lastLogEntry == "":
            print("Date of last log entry not found, writing one now and setting the var.")
            l.critical(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
        elif lastLogEntry + d.timedelta(hours=12) < d.datetime.now():
            l.critical(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
            lastLogEntry = d.datetime.now()
        try:
            if lastMailSent == "":
                sendEmailWarning(spec, desc)
                lastMailSent = d.datetime.now()
            elif lastMailSent + d.timedelta(days=1) < d.datetime.now():
                sendEmailWarning(spec, desc)
                lastMailSent = d.datetime.now()
        except Exception as e:
            print("Couldn't send email:", e)
    output = LOG_TEXT.format(desc=desc, percent=spec, status=status)
    print(output)