#! /bin/sh
# Get the file from the raspberrypi zero
curl http://calendarServer.home/kindle/done.png  -o status.png
# Clear the screen
eips -c
# Display the picture
eips -g status.png 
# Get the more detailed text file for reading
curl http://calendarServer.home/kindle/Cal.txt  -o  "/mnt/us/documents/events.txt" 
# All done