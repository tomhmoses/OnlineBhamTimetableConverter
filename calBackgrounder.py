import time
import BhamGoogleCalendarMaker
import BhamCalEmailSender
import pickle
import logging

# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

files = {"queue":"/home/tomhmoses/mysite_ttc/queue.pickle",
        "log":"/home/tomhmoses/mysite_ttc/backgrounder.log"}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler(files["log"])

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def main(logger = None):
    while True:
        time.sleep(5)
        queue = loadPickle(files["queue"])
        if len(queue) > 0:
            #details = [username, email, csv]
            details = queue[0]
            username = details[0]
            email = details[1].replace(" ", "")
            csv = details[2]
            print("Making calendar for " + username)
            linkToCal = BhamGoogleCalendarMaker.main(username, email, csv)
            print("about to send email")
            BhamCalEmailSender.sendMail(email, linkToCal)
            removeFromQueue()
            #60 second cooldown
            time.sleep(60)

def removeFromQueue():
    queue = loadPickle(files["queue"])

    if len(queue) == 1:
        queue = []
    elif len(queue) == 0:
        print("queue was already empty")
    else:
        queue = queue[1:]

    savePickle(files["queue"], queue)

def savePickle(file_name, obj):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj)

def loadPickle(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

if __name__ == "__main__":
    main()
