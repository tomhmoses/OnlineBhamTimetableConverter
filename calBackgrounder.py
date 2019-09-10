import time
import BhamGoogleCalendarMaker
import BhamCalEmailSender
import pickle
import config

# DEBUG: Detailed information, typically of interest only when diagnosing problems.

# INFO: Confirmation that things are working as expected.

# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.

# ERROR: Due to a more serious problem, the software has not been able to perform some function.

# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

files = {"queue":"/home/tomhmoses/mysite_ttc/queue.pickle",
        "log":"/home/tomhmoses/mysite_ttc/backgrounder.log"}

logger = logger = config.initilise_logging()

def main():
    while True:
        time.sleep(5)
        queue = loadPickle(files["queue"])
        if len(queue) > 0:
            #details = [username, email, csv]
            details = queue[0]
            username = details["username"]
            email = details["email"].replace(" ", "")
            csv = details["csv"]
            shortenTitle = details["shortenTitle"]
            customTitle = details["customTitle"]
            print("Making calendar for " + username + ", shortenTitle: " + str(shortenTitle) + ", customTitle: " + str(customTitle))
            linkToCal = BhamGoogleCalendarMaker.main(username, email, csv, shortenTitle, customTitle)
            if linkToCal:
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
