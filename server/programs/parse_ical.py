
from icalendar import Calendar
import urllib.request
import time
from datetime import datetime, timedelta, date
import codecs
import recurring_ical_events

print("Downloading the ICS file")

# You will need to add your private ical URL, 
# if you are using Google Calendar,please see:
# https://support.google.com/calendar/answer/37648?hl=en#zippy=%2Cget-your-calendar-view-only
#
#

ICAL_URL = ""

urllib.request.urlretrieve(ICAL_URL, "basic.ics")


cal = Calendar.from_ical(open('basic.ics','rb').read())

normal_events = []


start_date = datetime.now()
end_date =  datetime.now() + timedelta(days=28)

events = recurring_ical_events.of(cal).between(start_date, end_date)

for event in events:

    start = str(event["DTSTART"].dt)
    day = event["DTSTART"].dt.strftime("%d")
    niceDay = event["DTSTART"].dt.strftime("%a")
    niceTime = event["DTSTART"].dt.strftime("%H%M")
    name = str(event["SUMMARY"])

    # Bug fix...
    # Nice modern computers use fancy left and right quotes but that causes crashes
    # So if your event is something along the lines of ...Watch "The Longest Day"  
    # the program will crash.
    # So we need to fix this by replacing the nicely styled quotes 
    # with the more boring basic quotes
    
    left_quote_name=name.replace(chr(8220), chr(34))
    # Swapped the left quote for " now to the right but save a variable...
    name=left_quote_name.replace(chr(8221), chr(34))


    print(start, name)
    normal_events.append([start,name, day, niceTime, niceDay])

print("Got the information,now sorting it")
normal_events.sort()



# Add data to the SVG file
output = codecs.open('after-weather.svg', 'r', encoding='utf-8').read()

print("Creating the SVG file")

count = 0

start_date = str(start_date)

for event in normal_events:

    date_start = event[0]

    #Check that this is today's event
    if date_start[:10] == start_date[:10]:

        entry_time = event[3]
        entry_name = event[1] 

        if entry_time == "0000":
            entry_time="All day"

        # Escape special characters for rsvg-convert
        entry_name.replace("&", "&amp;")
        entry_name.replace("<", "&lt;")
        entry_name.replace(">", "&gt;")

        # Replace place holders with real information
        output = output.replace('hour'+ str(count) ,entry_time)
        output = output.replace('Name' + str(count) ,entry_name)

        count+=1

    #Only have space on the screen for the first 5 tasks...
    if (count == 5):

        break

#Erase unsused placehlders
output = output.replace('hour0' ,'')
output = output.replace('hour1' ,'')
output = output.replace('hour2' ,'')
output = output.replace('hour3' ,'')
output = output.replace('hour4' ,'')


output = output.replace('Name0' ,'')
output = output.replace('Name1' ,'')
output = output.replace('Name2' ,'')
output = output.replace('Name3' ,'')
output = output.replace('Name4' ,'')


# Write output
codecs.open('almost_done.svg', 'w', encoding='utf-8').write(output)

print("SVG Image Complete")

print("Writing the text file")
# Write the Calendar details to the text file
f = open("Cal.txt","w")

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
    if entry_date != previousDay:
 
       #Draw a line
        f.write("____________________________\n")
        f.write(txt_day_value+" ")
        f.write(txt_day+"\n\n")
        previous_day = entry_date
  
    entry_name = event[1] 

    # Write the details to the file
    if txt_time=="0000":
        f.write('All day event  \n')
    else:
        f.write(txt_time+"  ")
    
    f.write(entry_name+"\n")

f.close()
print("All done!")
