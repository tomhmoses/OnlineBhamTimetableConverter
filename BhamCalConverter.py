import BhamGetFrame
import BhamTTConverter
import BhamGoogleCalendarMaker
import getpass
import BhamCalEmailSender

def main():
    email, username, password = getUserInput()
    print(run(email, username, password))


def runFromFlask(email, username, password):
    print("running from flask")
    if email == "":
        print("uni email generated")
        email = username + "@student.bham.ac.uk"
    try:
        message = run(email, username, password)
    except Exception as e:
        message = str(e)
        message += "\nUsing:\n" + email + "\n" + username + "\n" + str(len(password) + ". Please try again in a minute..." )
    return  message


def run(email, username, password):
    frameSource, errorOccured = BhamGetFrame.getFrameSourceAnywhere(username, password)
    if errorOccured:
        print("error occurred in getting frame")
        errorMessage = frameSource
        return errorMessage
    saveToFile(frameSource, "frameSource.html")
    csv = BhamTTConverter.main(frameSource)
    saveToFile(csv, "Timetable.csv")
    linkToCal = BhamGoogleCalendarMaker.main(username, email, csv)
    BhamCalEmailSender.sendMail(email, linkToCal)
    return "done"


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
