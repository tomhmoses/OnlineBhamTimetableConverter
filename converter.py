# program to move bham timetable to google calendar (or other calendar)
# made by Tom Moses

def changeDateFormat(originalDate,monthDict):
    #start with 01 Oct 2018
    #end with 10/01/2018
    bits = originalDate.split(" ")
    newDate = monthDict[bits[1]]+"/"+bits[0]+"/"+bits[2]
    return newDate

def cutSectionFromText(text,startPosition,endPosition):
    text1 = text[:startPosition]
    text2 = text[endPosition:]
    return text1 + text2

def getTableFromFrame(text):
    #removes any new lines
    #method of removing linebreaks from https://tinyurl.com/y7ycqjll
    text =  text.replace('\n', '').replace('\r', '')
    #print "removed line breaks"
    #cuts off top
    startPosition = text.find("""<p><span class="labelone">""") - len("</table>")
    text = text[startPosition:]
    #print "removed start bit"
    #cuts off bottom
    endPosition = text.find("""<table class="footer-border-args" """)
    text = text[:endPosition]
    #print "removed end bit"
    
    #removes day bits
    #print "removing " + str(text.count("""<span class="labelone">""")) + " day title bits"
    while """<span class="labelone">""" in text:
        startPosition = text.find("</table>")
        #will then find if this day contains any info
        nextCloseTablePosition = text[startPosition+3:].find("</table>")+startPosition+3
        substring = text[startPosition+len("</table>"):nextCloseTablePosition]
        if "columnTitles"  in substring:
            #print "day contains info"
            endPosition = text[startPosition:].find("</tr>") + 5 + startPosition
        else:
            #print "day doesnt contain info"
            endPosition = text[startPosition+3:].find("</table>")+startPosition+3

        text = cutSectionFromText(text,startPosition,endPosition)
        #print "removed a day bit"
        #print startPosition
        #print endPosition
    #raw_input(text)
    return text


def Main(frameHTML):
    debug = False
    csv = "Start date,End date,Subject,Start Time,End Time,Location,Description"
    monthDict = {
        "Jan":"01",
        "Feb":"02",
        "Mar":"03",
        "Apr":"04",
        "May":"05",
        "Jun":"06",
        "Jul":"07",
        "Aug":"08",
        "Sep":"09",
        "Oct":"10",
        "Nov":"11",
        "Dec":"12"
    }


    #print "lets try and split the table into differnt events"
    #will import the html file as a string

    #print "got the HTML code"
    #we now have the full html of the body of the page, we need to cut it down.
    
    wholeTable = getTableFromFrame(frameHTML)
    #print "got the table from the HTML code"

    #splits at row breaks
    listOfRows = wholeTable.split("</tr><tr>")
    #print "split into "+str(len(listOfRows))+" different events"
    

    for eachEvent in listOfRows:
        eachEvent = eachEvent.replace("</td>","").replace("&amp;","&").replace("&nbsp;"," ").replace(",","")
        #splits at element break and removes first empty item from list
        eventInfoList = eachEvent.split("<td>")[1:]
        csvLine = "\n"
        #adds start and end date (which are the same)
        for count in range(2):
            csvLine += changeDateFormat(eventInfoList[0],monthDict) + ","
        #adds basic info
        for number in [1,3,4,5]:
            csvLine += eventInfoList[number] + ","
        #adds description
        if eventInfoList[6] != " ":
            csvLine += "With: " + eventInfoList[6] + ". "
        csvLine += "Activity: " + eventInfoList[1]
        csvLine += ". Type: " + eventInfoList[2]
        csvLine += ". Department: " + eventInfoList[7]
 
        csv += csvLine


    if debug:
        print csv

    return csv




if __name__ == "__main__":
  Main()