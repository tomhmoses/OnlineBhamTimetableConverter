from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pprint
import time
import logging

logger = logging.getLogger('cal_maker')
logger.setLevel(logging.WARN)
handler = logging.FileHandler(filename='calendar.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
            return create_calendar(username, email, csv, accountNo)
        except:
            logger.warn("failed with accountNo: " + str(accountNo))


def create_calendar(username, email, csv, account_no):
    store = file.Storage(filePaths[account_no]["token"])
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(filePaths[account_no]["creds"], SCOPES)
        creds = tools.run_flow(flow, store, args)
    service = build('calendar', 'v3', http=creds.authorize(Http()))



    summary = "UoB Timetable: " + username
    timeZone = "Europe/London"
    calendar = {
    'summary': summary,
    'timeZone': timeZone
    }
    logger.info("Creating calendar")
    created_calendar = service.calendars().insert(body=calendar).execute()
    calID = created_calendar["id"]
    csv_events = csv.split("\n")
    csv_events = csv_events[1:]
    counter = 0
    for csvEvent in csv_events:
        details = csvEvent.split(",")
        if to_date_time(details[0], details[3]) == "":
            logger.debug("error occurred setting datetime so skipped.")
        else:
            eventDetails = {
              'summary': details[2],
              'location': details[5],
              'description': details[6],
              'start': {
                'dateTime': to_date_time(details[0], details[3]),
                'timeZone': timeZone,
              },
              'end': {
                'dateTime': to_date_time(details[1], details[4]),
                'timeZone': timeZone,
              },
            }
            try:
                event = service.events().insert(calendarId=calID, body=eventDetails).execute()
                time.sleep(0.2)
                counter += 1
            except:
                logger.warn("failed making calendar with accountNo: " + str(counter))
    logger.info("uploaded " + str(counter) + "/" + str(len(csv_events)) + " events for " + username + " using account number: " + str(account_no))

    pp = pprint.PrettyPrinter(indent=4)

    rule = {
        'scope': {
            'type': 'default',
            'value': '',
        },
        'role': 'reader'
    }

    logger.debug("sleeping for 5 seconds...")
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

    logger.debug("sleeping for 5 seconds...")
    time.sleep(5)
    created_rule = service.acl().insert(calendarId=calID, body=rule).execute()
    pp.pprint(created_rule)
    #if this failed then perhaps a 5 second delay is too short.

    return "https://calendar.google.com/calendar/r?cid=" + calID


def to_date_time(date_string, time_string):
    date_arr = date_string.split("/")
    for count in range(len(date_arr)):
        while len(date_arr[count]) < 2:
            date_arr[count] = "0" + date_arr[count]
    time_arr = time_string.split(":")
    for count in range(len(time_arr)):
        while len(time_arr[count]) < 2:
            time_arr[count] = "0" + time_arr[count]
    dt_string = ""
    try:
        dt = datetime.datetime(year=date_arr[2], month=date_arr[0], day=date_arr[1], hour=time_arr[0], minute=time_arr[1], second=00)
        dt_string = dt.strftime("%Y-%m-%dT%H:%M:%S")
    except:
        logger.debug(date_arr)
        logger.debug(time_arr)
    return dt_string

if __name__ == '__main__':
    csv = "ok\n01/14/2019,01/14/2019,LC Logic & Computation(30180)/Lecture,12:00,13:00,Gisbert Kapp LT2 (E202),With:  . Activity: LC Logic & Computation(30180)/Lecture. Type: Lecture. Department: Computer Science"
    create_calendar("thm2000","thomas@tmoses.co.uk",csv,2)
