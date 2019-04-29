from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pprint
import time

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

args = tools.argparser.parse_args()
args.noauth_local_webserver = True

filePaths = [{"token":"/home/tomhmoses/mysite_ttc/token.json", "creds":"/home/tomhmoses/mysite_ttc/credentials.json"},
            {"token":"/home/tomhmoses/mysite_ttc/token2.json", "creds":"/home/tomhmoses/mysite_ttc/credentials2.json"},
            {"token":"/home/tomhmoses/mysite_ttc/token3.json", "creds":"/home/tomhmoses/mysite_ttc/credentials3.json"}]

def main(username, email, csv):
    for accountNo in range(len(filePaths)):
        try:
            return createCalendar(username, email, csv, accountNo)
        except:
            print("failed with accountNo: " + str(accountNo))


def createCalendar(username, email, csv, accountNo):
    store = file.Storage(filePaths[accountNo]["token"])
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(filePaths[accountNo]["creds"], SCOPES)
        creds = tools.run_flow(flow, store, args)
    service = build('calendar', 'v3', http=creds.authorize(Http()))



    summary = "UoB Timetable: " + username
    timeZone = "Europe/London"
    calendar = {
    'summary': summary,
    'timeZone': timeZone
    }
    print("about to make new calendar")
    created_calendar = service.calendars().insert(body=calendar).execute()
    calID = created_calendar["id"]
    csvEvents = csv.split("\n")
    csvEvents = csvEvents[1:]
    counter = 0
    for csvEvent in csvEvents:
        deets = csvEvent.split(",")
        if toDateTimeZ(deets[0], deets[3]) == "":
            print("error occurred setting datetime so skipped.")
        else:
            eventDetails = {
              'summary': deets[2],
              'location': deets[5],
              'description': deets[6],
              'start': {
                'dateTime': toDateTimeZ(deets[0], deets[3]),
                'timeZone': timeZone,
              },
              'end': {
                'dateTime': toDateTimeZ(deets[1], deets[4]),
                'timeZone': timeZone,
              },
            }
            try:
                event = service.events().insert(calendarId=calID, body=eventDetails).execute()
                time.sleep(0.2)
                counter += 1
            except:
                print("failed making calendar with accountNo: " + str(counter))
    print("uploaded " + str(counter) + "/" + str(len(csvEvents)) + " events for " + username + " using account number: " + str(accountNo))

    pp = pprint.PrettyPrinter(indent=4)

    rule = {
        'scope': {
            'type': 'default',
            'value': '',
        },
        'role': 'reader'
    }

    print("sleeping for 5 seconds...")
    time.sleep(5)
    created_rule = service.acl().insert(calendarId=calID, body=rule).execute()
    pp.pprint(created_rule)

    rule = {
        'scope': {
            'type': 'user',
            'value': email,
        },
        'role': 'owner'
    }

    print("sleeping for 5 seconds...")
    time.sleep(5)
    created_rule = service.acl().insert(calendarId=calID, body=rule).execute()
    pp.pprint(created_rule)
    #if this failed then perhaps a 5 second delay is too short.

    return "https://calendar.google.com/calendar/r?cid=" + calID


def toDateTimeZ(dateString, timeString):
    bitsOfDate = dateString.split("/")
    for count in range(len(bitsOfDate)):
        while len(bitsOfDate[count]) < 2:
            bitsOfDate[count] = "0" + bitsOfDate[count]
    bitsOfTime = timeString.split(":")
    for count in range(len(bitsOfTime)):
        while len(bitsOfTime[count]) < 2:
            bitsOfTime[count] = "0" + bitsOfTime[count]
    datetime = ""
    try:
        dt = datetime.datetime(year=bitsOfDate[2], month=bitsOfDate[0], day=bitsOfDate[1], hour=bitsOfTime[0], minute=bitsOfTime[1], second=00)
        datetime= dt.strftime("%Y-%m-%dT%H:%M:%S")
    except:
        print(bitsOfDate)
    return datetime

if __name__ == '__main__':
    csv = "ok\n01/14/2019,01/14/2019,LC Logic & Computation(30180)/Lecture,12:00,13:00,Gisbert Kapp LT2 (E202),With:  . Activity: LC Logic & Computation(30180)/Lecture. Type: Lecture. Department: Computer Science"
    createCalendar("thm2000","thomas@tmoses.co.uk",csv,2)
