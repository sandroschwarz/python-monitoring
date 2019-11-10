import logging as l # used for logging to file
import socket as s # used to get machine FQDN (displayed in the logs)
import datetime as d # for getting and formatting out own date display

LOG_FILENAME = d.datetime.now().strftime("%d-%m-%Y_%H-%M-%S.log") # Log will have a timestamp like this for its name
LOG_FORMAT = "%(asctime)s %(fqdn)s %(message)s" # Defining how the log will be contructed
LOG_TEXT = "{desc} usage is: {percent}% ({status})" # Setting out custom log message text for reusing it later
LOG_DATEFORMAT = "%d.%m.%Y %H:%M:%S" # This will be our displayed timestamp in the log

MACHINE_FQDN = s.getfqdn()
MAP = {"fqdn": MACHINE_FQDN} # used for formatting log lines



# Basic log configuration, including log name, level of logging (set to DEBUG to get nominal stats as well)
l.basicConfig(
    format=LOG_FORMAT,
    datefmt=LOG_DATEFORMAT,
    filename=LOG_FILENAME,
    filemode='w',
    level=l.WARNING
)

# Main function for checking against soft and hard limits, logging accordingly and sending warnings
def specStat(spec, desc):
    status = ""
    if 0 <= spec <= 80:
        status = "nominal"
        l.info(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
    elif 80 < spec < 90:
        status = "warning"
        l.warning(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
    else:
        status = "critical"
        l.critical(LOG_TEXT.format(desc=desc, percent=spec, status=status), extra=MAP)
        # SEND EMAIL
    print(LOG_TEXT.format(desc=desc, percent=spec, status=status))