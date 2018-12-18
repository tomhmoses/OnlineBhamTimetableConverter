import BhamGetFrame
import BhamTTConverter
import BhamGoogleCalendarMaker
import getpass
import BhamCalEmailSender
import DonationChecker
import pickle
from validate_email import validate_email

visitsFilePath = "visits.pickle"
usernameLogFilePath = "usernameLog.txt"
inUseFilePath = "inUse.pickle"
queueFilePath = "queue.pickle"
warningFilePath = "siteWarning.txt"
freeUsersFilePath = "freeUsers.txt"

MINS_PER_USER = 20

def resetInUse():
    inUse = False
    savePickle(inUseFilePath, inUse)

def setInUse():
    inUse = True
    savePickle(inUseFilePath, inUse)

def main():
    email, username, password = getUserInput()
    print(run(email, username, password))

def runFromFlaskWithDB(email, username, password):
    print("running from flask")
    mins = 0
    username = checkUsername(username)
    if username == "Invalid username":
        return username, mins
    if loadPickle(inUseFilePath):
        print("was in use :(")
        message = "Somebody else is using the service right now. Please try again in 10 seconds..."
    else:
        setInUse()
        if email == "":
            print("uni email generated")
            email = username + "@student.bham.ac.uk"
        validEmail = validate_email(email)
        if username in getFreeUsers():
            donated = True
        else:
            donated = DonationChecker.checkForDonationAnywhere(username)
        if not donated:
            return "It looks like you haven't donated yet. Please do that first. If you are sure you have donated and you are still getting this error please email me.", 0
        if validEmail:
            try:
                message, mins = runWithDB(email, username, password)
            except Exception as e:
                message = str(e)
                message += "\nUsing:\n" + email + "\n" + username + "\n" + str(len(password)) + ". Please try again in 10 seconds..."
            finally:
                resetInUse()
        else:
            message = "Invalid email, please try again..."
            resetInUse()
    return message, mins

def checkUsername(username):
    if "@" in username:
        username = username[:username.find("@")]
    username = username.replace(" ", "")
    for char in username:
        if not (char.isalpha() or char.isdigit()):
            return "Invalid username"
    return username


def run(email, username, password):
    frameSource, errorOccured = BhamGetFrame.getFrameSourceAnywhere(username, password)
    if errorOccured:
        print("error occurred in getting frame")
        errorMessage = frameSource
        return errorMessage
    print("got frame source")
    saveToFile(frameSource, "frameSource.html")
    csv = BhamTTConverter.main(frameSource)
    print("generated csv")
    saveToFile(csv, "Timetable.csv")
    linkToCal = BhamGoogleCalendarMaker.main(username, email, csv)
    BhamCalEmailSender.sendMail(email, linkToCal)
    return "done"

def runWithDB(email, username, password):
    frameSource, errorOccured = BhamGetFrame.getFrameSourceAnywhere(username, password)
    if errorOccured:
        print("error occurred in getting frame.. trying again")
        errorMessage = frameSource
        if "Login Error." in errorMessage:
            return errorMessage, 0
        else:
            frameSource, errorOccured = BhamGetFrame.getFrameSourceAnywhere(username, password)
            if errorOccured:
                print("error occurred in getting frame.. again")
                errorMessage = frameSource
                return errorMessage, 0
    print("got frame source")
    #saveToFile(frameSource, "frameSource.html")
    csv = BhamTTConverter.main(frameSource)
    print("generated csv")
    #saveToFile(csv, "Timetable.csv")
    queueLength = addToDB(username, email, csv)
    #linkToCal = BhamGoogleCalendarMaker.main(username, email, csv)
    #BhamCalEmailSender.sendMail(email, linkToCal)
    return "done" , queueLength * MINS_PER_USER

def addToDB(username, email, csv):
    try:
        queue = loadPickle(queueFilePath)
        details = [username, email, csv]
        queue.append(details)
        savePickle(queueFilePath, queue)
        return len(queue)
    except:
        return 0

def getStats():
    try:
        visits =  loadPickle(visitsFilePath)
    except:
        visits = 0
    try:
        file = open(usernameLogFilePath, "r")
        usernames = file.readlines()
        file.close()
        users = len(usernames)
    except:
        visits = 0
    try:
        queue = loadPickle(queueFilePath)
        queueLen = len(queue)
    except:
        queue = 0
    stats = {"visits":visits, "users":users, "queue":queueLen}
    return stats

def getWarningMessage():
    try:
        file = open(warningFilePath, "r")
        warning = file.read()
        file.close()
    except:
        warning = ""
    return warning

def trackVisit():
    attempts = 3
    worked = False
    while attempts > 0 and worked == False:
        try:
            trackVisitWithPickle()
            worked = True
        except:
            attempts -= 1
    if not worked:
        print("failed to track site visit")

def trackVisitWithPickle():
    visits = loadPickle(visitsFilePath)
    visits += 1
    savePickle(visitsFilePath, visits)

def savePickle(file_name, obj):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj)

def loadPickle(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)


def saveToFile(text, filePath = "output.txt"):
    file = open(filePath, "w")
    file.write(text)
    file.close()

def getFreeUsers():
    file = open(freeUsersFilePath, "r")
    contents = file.readlines()
    file.close()
    return contents

def getUserInput():
    print("\nYou will be emailed the calendar as it takes a minute or two to generate.")
    print("If you want to use your UoB student email address, leave this field blank.\n")
    usingStudentMail = False
    email = input("Please enter your email: ")
    if email == "":
        email2 = ""
        usingStudentMail = True
    else:
        email2 = input("Please confirm your email: ")
    while email != email2:
        print("\nSorry, those emails didn't match. Please try again.")
        email = input("Please enter your email: ")
        if email == "":
            email2 = ""
            usingStudentMail = True
        else:
            email2 = input("Please confirm your email: ")
    username = input("Please enter your UoB username: ")
    if usingStudentMail:
        email = username + "@student.bham.ac.uk"
    password = getpass.getpass("Please enter your UoB password: ")
    return email, username, password


if __name__ == '__main__':
    main()
