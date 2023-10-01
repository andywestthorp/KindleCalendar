# KindleCalendar
Show your iCal on your old kindle

Acknowledgements

This is based on the work of Pablo Jiménez Mateo  https://github.com/pablojimenezmateo/kindle-wallpaper which is based on the work of Matthew Petroff: http://www.mpetroff.net/archives/2012/09/14/kindle-weather-display/

It also used code from Matt Healy https://github.com/lankybutmacho/web-to-kindle-heroku/tree/main

I had an old kindle knocking about in a drawer and thought it would be nice to use the screen to show upcoming calendar events for today. 

Obviously, I wasn't the first person to think of this and I am grateful to Pablo and Matthew for their work.

I have modified Pablo's script to add all day and recurring events and I have added an extra feature to create a text file of the next 4 week's worth of calendar events.

crontab e

*/10 * * * * /home/pi/kindle/server/launch.sh


Feel free to copy and use as you wish.

Andy Westthorp
5th August 2023
