import time
import BhamGoogleCalendarMaker
import BhamCalEmailSender
import pickle

queueFilePath = "/home/tomhmoses/mysite/queue.pickle"

def main():
    while True:
        time.sleep(5)
        queue = loadPickle(queueFilePath)
        if len(queue) > 0:
            #details = [username, email, csv]
            details = queue[0]
            username = details[0]
            email = details[1]
            csv = details[2]
            print("Making calendar for " + username)
            linkToCal = BhamGoogleCalendarMaker.main(username, email, csv)
            BhamCalEmailSender.sendMail(email, linkToCal)
            removeFromQueue()

def removeFromQueue():
    queue = loadPickle(queueFilePath)

    if len(queue) == 1:
        queue = []
    elif len(queue) == 0:
        print("queue was already empty")
    else:
        queue = queue[1:]

    savePickle(queueFilePath, queue)

def savePickle(file_name, obj):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj)

def loadPickle(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

if __name__ == "__main__":
    main()
