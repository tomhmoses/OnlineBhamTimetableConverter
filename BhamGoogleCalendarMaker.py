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

def main(username, email, csv):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store, args)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    #events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                    maxResults=10, singleEvents=True,
    #                                    orderBy='startTime').execute()
    #events = events_result.get('items', [])

    #if not events:
    #    print('No upcoming events found.')
    #for event in events:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print(start, event['summary'])

    summary = "UoB Timetable: " + username
    timeZone = "Europe/London"
    calendar = {
    'summary': summary,
    'timeZone': timeZone
    }
    #print("about to make new calendar")
    created_calendar = service.calendars().insert(body=calendar).execute()
    calID = created_calendar["id"]
    csvEvents = csv.split("\n")
    #print(csvEvents)
    #scvEvents = csvEvents[1:]
    #print(csvEvents)
    counter = 0
    for csvEvent in csvEvents:
        #print("doing loop")
        deets = csvEvent.split(",")
        if toDateTimeZ(deets[0], deets[3]) == "":
            myLog("error occurred setting datetime so skipped.")
        else:
            #print(timeformat)
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
                time.sleep(20)
                counter += 1
            except:
                pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(eventDetails)
    print("uploaded " + str(counter) + "/" + str(len(csvEvents)) + " events for " + username)

    pp = pprint.PrettyPrinter(indent=4)

    rule = {
        'scope': {
            'type': 'default',
            'value': '',
        },
        'role': 'reader'
    }

    print("sleeping for 20 seconds...")
    time.sleep(20)
    created_rule = service.acl().insert(calendarId=calID, body=rule).execute()
    pp.pprint(created_rule)

    rule = {
        'scope': {
            'type': 'user',
            'value': email,
        },
        'role': 'owner'
    }

    print("sleeping for 20 seconds...")
    time.sleep(20)
    created_rule = service.acl().insert(calendarId=calID, body=rule).execute()
    pp.pprint(created_rule)

    return "https://calendar.google.com/calendar/r?cid=" + calID

def myLog(text):
    doesNothing = text

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
        datetime += bitsOfDate[2] + "-" + bitsOfDate[0] + "-" + bitsOfDate[1] + "T"
        datetime += bitsOfTime[0] + ":" + bitsOfTime[1] + ":00Z"
    except:
        print(bitsOfDate)
    return datetime

if __name__ == '__main__':
    main()
