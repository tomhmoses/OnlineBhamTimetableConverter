# OnlineBhamTimetableConverter
This will automatically add your bham timetable to a google calendar and email you a link that gives you control permission over it.

Use this service at the link in the next section.

Feel free to fork it if you want to make improvements.
To get this to work you may need to change a few string where I mention `bham.timetable@gmail.com` and you will be asked to authorise this with your google account through the google api. I recommend making a new google account for this project to create calendars and emails with. You will need to create a new project through the google API dashboard and add its `credentials.json` file to the root directory of this project.


# Example
Visit [my website](https://ttc.tmoses.co.uk) to see it on action.


# What happens
- The user enters their details into my website running through flask. These details are then validated and passed into the main program:
- The university timetable website is loaded, logged into, and the html is scraped.
- This is then parsed and turned into a CSV of all the found events.
- This is passed to another python program where a new google calendar is created and all the events are added to it, using the google api
- This calendar is made public and owership permissions are given to the email the user gave. This means that if the user gave their google account email then it is automatically shared with them in this process.
- The user is then sent a HTML email with a link to view the new calendar.
  - <details>
    <summary>Example email</summary>

    <a href="https://ibb.co/ggWcxhZ"><img src="https://i.ibb.co/ggWcxhZ/CC5-C9-AD2-AA69-44-B1-9-C9-B-93-A44489085-F.jpg" alt="example email screenshot" border="0" /></a>
    
    </details>

