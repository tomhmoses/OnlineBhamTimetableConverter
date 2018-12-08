import BhamGetFrame
import BhamTTConverter
import BhamGoogleCalendarMaker
import getpass
import BhamCalEmailSender
import pickle

visitsFilePath = "visits.pickle"
usernameLogFilePath = "usernameLog.txt"
inUseFilePath = "inUse.pickle"

def resetInUse():
    inUse = False
    savePickle(inUseFilePath, inUse)

def setInUse():
    inUse = True
    savePickle(inUseFilePath, inUse)

def main():
    email, username, password = getUserInput()
    print(run(email, username, password))


def runFromFlask(email, username, password):
    print("running from flask")
    username = checkUsername(username)
    if username == "Invalid username":
        return username
    if loadPickle(inUseFilePath):
        print("was in use :(")
        message = "Somebody else is using the service right now. Due to limitation with having a free google API account I can't handle more than one request at once. Please try again in 2 minutes..."
    else:
        setInUse()
        if email == "":
            print("uni email generated")
            email = username + "@student.bham.ac.uk"
        try:
            message = run(email, username, password)
        except Exception as e:
            message = str(e)
            message += "\nUsing:\n" + email + "\n" + username + "\n" + str(len(password)) + ". Please try again in 2 minutes..."
        finally:
            resetInUse()
    return message

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

def getStats():
    try:
        visits = visits = loadPickle(visitsFilePath)
    except:
        visits = 0
    try:
        file = open(usernameLogFilePath, "r")
        usernames = file.readlines()
        file.close()
        users = len(usernames)
    except:
        visits = 0
    stats = {"visits":visits, "users":users}
    return stats

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
