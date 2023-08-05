import urllib.request, json 
from datetime import date
import codecs
import os

# API key - Get your own from https://openweathermap.org
API_KEY = ""


# Read the JSON
with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?lat=55.644675&lon=-2.3355743&appid=" + API_KEY + "&units=metric") as url:
    data = json.loads(url.read().decode())

# Get API info
low   = data["main"]["temp_min"]
high  = data["main"]["temp_max"]
image = data["weather"][0]["id"]


# This tells if it is night "n" or day "d"
light = data["weather"][0]["icon"][-1:]
#light = "n"

# Extra info
date = date.today().strftime("%d %b %Y")

# Get the correct icon
image_path = 'icons/' + str(image) + light + '.svg'

# Open SVG to process
output = codecs.open('icons/template.svg', 'r', encoding='utf-8').read()

# Read icon (Just the path line)
if os.path.exists(image_path):
    f = codecs.open(image_path, 'r', encoding='utf-8')
    f.readline()
    icon = f.readline()
    print(image_path)
    f.close()
else: # Error handling
    f = codecs.open('icons/error.svg', 'r', encoding='utf-8')
    f.readline()
    icon = f.readline()
    f.close()

# Insert icons and temperatures
output = output.replace('TODAY',date)
output = output.replace('ICON_ONE', icon)
output = output.replace('HIGH_ONE',"{:2.1f}".format(high))
output = output.replace('LOW_ONE',"{:2.1f}".format(low))

# Write output
codecs.open('after-weather.svg', 'w', encoding='utf-8').write(output)
