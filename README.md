# OnlineBhamTimetableConverter
Will automatically add your bham timetable to a google calendar and email you a link that gives you control permission over it.

To get this to work you may need to change a few string where I mention `bham.timetable@gmail.com` and you will be asked to authorise this with your google account through the google api. I recoomend making a new google account for this project to create calendars and emails with. You will need to create a new project through the google API dashboard and add its `credentials.json` file to the root directory of this project.


# Example
Visit [my pythonanywhere site to see it on action](https://tomhmoses.pythonanywhere.com/timetable/).

As of writing this README, it currently fully works!

(thanks to the pytonanywhere team for helping me [solve some issues](https://www.pythonanywhere.com/forums/topic/13594/))

# What happens
The user enters their details into my website running through flask. These details are then validated and passed into the main program:
- The university timetable website is loaded, logged into, and the html is scraped
- This is then parsed and turned into a CSV of all the found events
- This is passed to another python program where a new google calendar is created and all the events are added to it, using the google api
- This calendar is made public and owership permissions are given to the email the user gave. This means that if the user gave their google account email then it is automatically shared with them in this process.
- The user is then sent a HTML email with a link to view the new calendar as can be seen below:

![alt text](https://tinyurl.com/yaqw4tou "Example email")
