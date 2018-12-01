from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def main(username, csv):
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
        creds = tools.run_flow(flow, store)
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

    summary = "UoB Calendar: " + username
    timeZone = "Europe/London"
    calendar = {
    'summary': summary,
    'timeZone': timeZone
    }

    created_calendar = service.calendars().insert(body=calendar).execute()
    calID = created_calendar["id"]
    csvEvents = csv.split("/n")
    for csvEvent in csvEvents:
        deets = csvEvent.split(",")
        event = {
          'summary': deets[2],
          'location': deets[5],
          'description': deets[6],
          'start': {
            'dateTime': toDateTime(deets[0], deets[3]),
            'timeZone': timeZone,
          },
          'end': {
            'dateTime': toDateTime(deets[1], deets[4]),
            'timeZone': timeZone,
          },
        }
        event = service.events().insert(calendarId=calID, body=event).execute()

def toDateTime(dateString, timeString):
    bitsOfTime = timeString.split(":")
    bitsOfDate = dateString.split("/")
    datetime = bitsOfDate[2] + "-" + bitsOfDate[0] + "-" + bitsOfDate[1] + "T"
    datetime += bitsOfTime[0] + ":" + bitsOfTime[1] + ":00Z"

if __name__ == '__main__':
    main()