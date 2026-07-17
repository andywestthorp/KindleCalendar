import codecs
from datetime import datetime, timedelta, date
import html
import urllib.request

from anyascii import anyascii
from icalendar import Calendar
import recurring_ical_events

# --- Configuration ---
ICAL_URL = "https://calendar.google.com/calendar/ical/qq50na1h7t2h12j3p5qhntqphs%40group.calendar.google.com/private-6b90ee1476f62c7bdb66975e80cefa6b/basic.ics"


# --- Helper Functions ---
def get_ordinal_suffix(day_str: str) -> str:
    """Returns the day with its appropriate English ordinal suffix (e.g. '27' -> '27th')."""
    day = int(day_str)
    if 11 <= day <= 13:
        return f"{day}th"
    
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    return f"{day}{suffixes.get(day % 10, 'th')}"


def get_line_id(count: int) -> str:
    """
    Converts line index numbers (0 to 12) into SVG placeholder suffixes.
    Indexes 0-9 output '0'-'9'. Indexes 10, 11, 12 output 'A', 'B', 'C'.
    """
    return f"{count:X}"


# --- 1. Fetch & Parse Calendar ---
print("Downloading the ICS file")
urllib.request.urlretrieve(ICAL_URL, "basic.ics")

print("Parsing the iCal entries")
with open("basic.ics", "rb") as ics_file:
    cal = Calendar.from_ical(ics_file.read())

start_date = datetime.now()
end_date = start_date + timedelta(days=28)
events = recurring_ical_events.of(cal).between(start_date, end_date)

normal_events = []
for event in events:
    start = str(event["DTSTART"].dt)
    day = event["DTSTART"].dt.strftime("%d")
    nice_day = event["DTSTART"].dt.strftime("%a")
    nice_time = event["DTSTART"].dt.strftime("%H%M")
    
    # Sanitize name to pure ASCII
    name = anyascii(str(event["SUMMARY"]))
    
    normal_events.append([start, name, day, nice_time, nice_day])

print("Got the information, now sorting it")
normal_events.sort()


# --- 2. Process & Generate SVG ---
print("Creating the SVG file")
with codecs.open("template.svg", "r", encoding="utf-8") as template_file:
    output = template_file.read()

# Set the SVG master header date
top_line_date = date.today().strftime("%A - %d %b %Y")
output = output.replace("TopLine(23Characters)", top_line_date)

count = 0
yesterday = str(start_date)[:10]

for event in normal_events:
    date_start, entry_name, day_num, entry_time, entry_day = event
    
    if entry_time == "0000":
        entry_time = "All day"

    # Clean XML/HTML characters
    entry_name = html.escape(entry_name)
    today = date_start[:10]

    # Detect when a new day header needs to be inserted
    if today != yesterday:
        print("New day...")
        
        # Format the header to: "[Mon - 27th]"
        formatted_day = get_ordinal_suffix(day_num)
        new_day_header = f"[{entry_day} - {formatted_day}]"
        
        line_id = get_line_id(count)
        output = output.replace(f"line{line_id}", new_day_header)
        print(f"line{line_id} is now {new_day_header}")
        
        count += 1
        yesterday = today

    # Replace line with actual schedule entry
    line_id = get_line_id(count)
    output = output.replace(f"line{line_id}", f"{entry_time}: {entry_name}")
    print(f"line{line_id} is now {entry_time}: {entry_name}")
    
    count += 1
    
    # Quit if SVG space is exhausted (0-12)
    if count >= 13:
        break

# Clear remaining/unused line placeholders
for i in range(13):
    line_id = get_line_id(i)
    output = output.replace(f"line{line_id}", "")

# Save final SVG output
with codecs.open("almost_done.svg", "w", encoding="utf-8") as output_file:
    output_file.write(output)

print("SVG Image Complete")


# --- 3. Generate Calendar Text File ---
print("Writing the text file")
with open("Cal.txt", "w") as text_file:
    text_file.write("Upcoming calendar events\n========================\n\n")
    
    if normal_events:
        previous_day = str(normal_events[0][0])[:10]
        print(f"Previous day = {previous_day}")

        for event in normal_events:
            entry_date, entry_name, day_num, entry_time, entry_day = event
            entry_date = entry_date[:10]

            # Section separator for a new day
            if entry_date != previous_day:
                text_file.write("____________________________\n")
                formatted_day = get_ordinal_suffix(day_num)
                text_file.write(f"{entry_day} - {formatted_day}\n\n")
                previous_day = entry_date

            # Write event details
            time_display = "All day event  " if entry_time == "0000" else f"{entry_time}  "
            text_file.write(f"{time_display}{entry_name}\n")

print("All done!")