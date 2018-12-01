import getFrame
import converter

def main():
    username = raw_input("Please enter your username: ")
    password = raw_input("Please enter your password: ")
    frameSource, errorOccured = getFrame.getFrameSource(username, password)
    if errorOccured:
        errorMessage = frameSource
        print errorMessage
        quit()
    csv = converter.Main(frameSource)
    saveToFile(csv, "Timetable.csv")

def saveToFile(text, filePath = "output.txt"):
    file = open(filePath, "w")
    file.write(text)
    file.close()



if __name__ == '__main__':
    main()