from icalendar import Calendar
import urllib.request
import time
from datetime import datetime, timedelta, date

import recurring_ical_events


# This is based on the ical.py file and we already have the basic.ics file downloaded, 
# we won't waste time doing that again!

print("Using the Downloaded ICal")

cal = Calendar.from_ical(open('basic.ics','rb').read())

normal_events = []

start_date = datetime.now()
end_date =  datetime.now() + timedelta(days=28) # 4 weeks but feel free to change this.

events = recurring_ical_events.of(cal).between(start_date, end_date)

for event in events:

    start = str(event["DTSTART"].dt)
    day = event["DTSTART"].dt.strftime("%d")
    nice_day = event["DTSTART"].dt.strftime("%a")
    nice_time = event["DTSTART"].dt.strftime("%H%M")
    name = str(event["SUMMARY"])
    print(start, name)
    normal_events.append([start,name, day, nice_time, nice_day])

print("Got the information,now sorting it")
normal_events.sort()

print("Writing the file")
# Write the Calendar details to the text file
f = open("Cal.txt","w")

count = 0
print("Writing today's events to the file")

f.write("Upcoming calendar events\n")
f.write("========================\n")
f.write("\n")

previous_day=str(normal_events[0])
previous_day=previous_day[2:12]
print("Previous day = ",previous_day)

for event in normal_events:

    entry_date = str(event[0])

    if len(entry_date) > 10: 
        # Chop duration as not really needed
        entry_date = entry_date[:10]

    print(entry_date)

    txt_day = str(event[2])
    txt_time = str(event[3])
    txt_day_value = str(event[4])

    # Checking for a new day - add a line to separate
    if entry_date != previous_day:
 
        f.write("____________________________\n")
        f.write(txt_day_value+" ")
        f.write(txt_day+"\n\n")
        previous_day = entry_date
  
    entry_name = event[1] 

    if txt_time=="0000":
        f.write('All day event  \n')
    else:
        f.write(txt_time+"  ")
    
    f.write(entry_name+"\n")

print("All done!")
f.close()
