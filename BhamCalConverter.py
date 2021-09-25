import BhamGetFrame
import BhamTTConverter
import BhamGoogleCalendarMaker
import getpass
import BhamCalEmailSender
import pickle
import datetime
from validate_email import validate_email

files = {
    "visits":"visits.pickle",
    "usernameLog":"usernameLog.txt",
    "inUse":"inUse.pickle",
    "queue":"queue.pickle",
    "warning":"warningMessage.txt",
    "info":"infoMessage.html",
    "freeUsers":"freeUsers.txt",
    "linesOfCode":"linesOfCode.pickle",
    "CAPTCHASecretKey":"CAPTCHASecretKey.txt",
    "normalLog":"normal.log",
    "debugLog":"debug.log",
    "jumpHistory":"jumps.csv",
    "cachedStats":"cachedStats.pickle"
}

MINS_PER_USER = 5

def resetInUse():
    inUse = False
    savePickle(files["inUse"], inUse)

def setInUse():
    inUse = True
    savePickle(files["inUse"], inUse)

def main():
    email, username, password = getUserInput()
    print(run(email, username, password))

def runFromFlaskWithDB(email, username, password, shortenTitle, customTitle):
    print("running from flask with username:" + username)
    mins = 0
    username = checkUsername(username)
    if username == "Invalid username":
        return username, mins
    if loadPickle(files["inUse"]):
        print("was in use :(")
        message = "Somebody else is using the service right now. Please try again in 10 seconds..."
    else:
        setInUse()
        if email == "":
            print("uni email generated")
            email = username + "@student.bham.ac.uk"
        else:
            email = tryToFixEmail(email)
        validEmail = validate_email(email)
        if validEmail:
            try:
                message, mins = runWithDB(email, username, password, shortenTitle, customTitle)
            except Exception as e:
                message = str(e)
                message += "\nUsing:\n" + email + "\n" + username + "\n" + str(len(password)) + ". Please try again in 10 seconds..."
            finally:
                resetInUse()
        else:
            message = "Invalid email, please try again..."
            resetInUse()
    return message, mins

def runFromFlask2019(email, username, password):
    queueLength = -1
    print("running from flask with username:" + username)
    # validation
    username = checkUsername(username)
    if username == "Invalid username":
        return "Error: Invalid username!", None
    elif not validate_email(email) or "." not in email[email.find("@"):]:
        return "Error: Invalid email!", None
    if loadPickle(files["inUse"]):
        print("was in use :(")
        message = "Somebody else is using the service right now. Please try again in 10 seconds..."
    else:
        setInUse()
        try:
            message, queueLength = runWithDB(email, username, password, True, "UoB Timetable " + username + " " + str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M')))
        except Exception as e:
            message = str(e)
            message += "\nUsing:\n" + email + "\n" + username + "\n" + str(len(password)) + ". Please try again in 10 seconds..."
        finally:
            resetInUse()
    return message, queueLength

def queueJump(username, person, password, how):
    f=open(files["jumpHistory"],"a+")
    f.write("%s,%s,%s,%s\r\n" % (username, person, password, how))
    f.close()
    if "in" not in password: #well done, you found the password
        return "wrong password"
    else:
        toMove = None
        toFind = username
        queue = loadPickle(files["queue"])
        for count in range(len(queue)):
            if queue[count]["username"].lower() == toFind.lower():
                toMove = count
        if not toMove:
            return "could not find user"
        else:
            newQueue = []
            newQueue.append(queue[0])
            newQueue.append(queue[toMove])
            for count in range(1, len(queue)):
                if count != toMove:
                    newQueue.append(queue[count])
            savePickle(files["queue"], newQueue)
            return "moved " + username + " to the front!"

def checkUsername(username):
    if "@" in username:
        username = username[:username.find("@")]
    username = username.replace(" ", "")
    for char in username:
        if not (char.isalpha() or char.isdigit()):
            return "Invalid username"
    return username

def tryToFixEmail(email):
    email = email.lower()
    origEmail = email
    email = email.replace("students.", "student.")
    email = email.replace(".bhan.", ".bham.")
    email = email.replace("bham.student", "student.bham")
    email = email.replace("bham.student", "student.bham")
    email = email.replace("student.ac", "student.bham.ac")
    email = email.replace("gmail.co.uk", "gmail.com")
    return email

#def run(email, username, password):
#    frameSource, errorOccured = BhamGetFrame.getFrameSourceAnywhere(username, password)
#    if errorOccured:
#        print("error occurred in getting frame")
#        errorMessage = frameSource
#        return errorMessage
#    print("got frame source")
#    saveToFile(frameSource, "frameSource.html")
#    print("saved frame source to file")
#    csv = BhamTTConverter.main(frameSource)
#    print("generated csv")
#    saveToFile(csv, "Timetable.csv")
#    linkToCal = BhamGoogleCalendarMaker.main(username, email, csv)
#    BhamCalEmailSender.sendMail(email, linkToCal)
#    return "done"

def runWithDB(email, username, password, shortenTitle, customTitle):
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
    print("got frame source in BhamCalConverter.py runWithDB")
    #saveToFile(frameSource, "frameSource.html")
    csv = BhamTTConverter.main(frameSource)
    print("generated csv")
    #saveToFile(csv, "Timetable.csv")
    queueLength = addToDB(username, email, csv, shortenTitle, customTitle)
    print("added to queue")
    #linkToCal = BhamGoogleCalendarMaker.main(username, email, csv)
    #BhamCalEmailSender.sendMail(email, linkToCal)
    return "done" , queueLength

def addToDB(username, email, csv, shortenTitle, customTitle):
    try:
        print("about to load pickle")
        queue = loadPickle(files["queue"])
        print("loaded pickle")
        details = {"username":username, "email":email, "csv":csv, "shortenTitle":shortenTitle, "customTitle":customTitle}
        queue.append(details)
        print("about to save pickle")
        savePickle(files["queue"], queue)
        print("saved pickle")
        return len(queue)
    except Exception as e:
        print(e)
        return 0

def getStats():
    try:
        visits =  loadPickle(files["visits"])
    except:
        visits = -1
    try:
        file = open(files["usernameLog"], "r")
        usernames = file.readlines()
        file.close()
        users = len(usernames)
        diffUsernames = []
        myUses = 0
        matthew = 0
        prev = ""
        uses = 0
        for username in usernames:
            if username.lower() not in diffUsernames:
                diffUsernames.append(username.lower())
            if "thm837" in username.lower():
                myUses += 1
            elif "mlb801" in username.lower():
                matthew += 1
            if prev != username.lower():
                uses += 1
                prev = username.lower()
        diffUsers = len(diffUsernames)
    except:
        users = -1
        diffUsers = -1
        myUses = -1
        matthew = -1
        uses = -1
    try:
        queue = loadPickle(files["queue"])
        queueLen = len(queue)
        queueList = []
        for each in queue:
            queueList.append(each["username"])
    except:
        queueList=["failed"]
        queueLen = -1
    try:
        linesOfCodeDic = loadPickle(files["linesOfCode"])
        HTML = linesOfCodeDic["HTML"]
        python = linesOfCodeDic["python"]
    except:
        HTML = -1
        python = -1
    stats = {"visits":visits, "users":users, "uses":uses, "diffUsers":diffUsers, "myUses":myUses, "queue":queueLen, 'HTML':HTML, 'python':python, 'matthew':matthew, 'queueList':queueList}
    saveCachedStats(stats)
    return stats

def saveCachedStats(stats):
    uses = stats["uses"]
    diffUsers = stats["diffUsers"]
    visits = stats["visits"]
    cachedStats = {}
    cachedStats["formattedUses"] = f"{uses:,}"
    cachedStats["formattedUsers"] = f"{diffUsers:,}"
    cachedStats["formattedVisits"] = f"{visits:,}"
    savePickle(files["cachedStats"], cachedStats)

def getCachedStats():
    cachedStats = loadPickle(files["cachedStats"])
    return cachedStats

def getFileContents(filePath):
    try:
        file = open(filePath, "r")
        contents = file.read()
        file.close()
    except:
        contents = ""
    return contents

def getWarningMessage():
    return getFileContents(files["warning"])

def getInfoMessage():
    return getFileContents(files["info"])

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
    visits = loadPickle(files["visits"])
    visits += 1
    savePickle(files["visits"], visits)

def savePickleForHuman(file_name, obj):
    savePickle(file_name, obj, protocol=0)

def savePickle(file_name, obj, protocol=pickle.DEFAULT_PROTOCOL):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj, protocol)

def loadPickle(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)

def getCAPTCHASiteKey():
    return "6LekpIQUAAAAAM-ECLqHuBs7uRdEe5oxug31idbQ"

def getCAPTCHASecretKey():
    return getFileContents(files["CAPTCHASecretKey"]).strip()

def saveToFile(text, filePath = "output.txt"):
    file = open(filePath, "w")
    file.write(text)
    file.close()

def getUserInput():
    print("\nYou will be emailed the calendar as it takes a minute or two to generate.")
    print("If you want to use your UoB student email address, leave this field blank.\n")
    usingStudentMail = False
    email1 = input("Please enter your email: ")
    if email1 == "":
        email2 = ""
        usingStudentMail = True
    else:
        email2 = input("Please confirm your email: ")
    while email1 != email2:
        print("\nSorry, those emails didn't match. Please try again.")
        email1 = input("Please enter your email: ")
        if email1 == "":
            email2 = ""
            usingStudentMail = True
        else:
            email2 = input("Please confirm your email: ")
    username = input("Please enter your UoB username: ")
    if usingStudentMail:
        email1 = username + "@student.bham.ac.uk"
    password = getpass.getpass("Please enter your UoB password: ")
    return email1, username, password


if __name__ == '__main__':
    #print(queueJump("thm8377", "bingo", "gone", "main method"))
    print(validate_email("good@gmail"))







