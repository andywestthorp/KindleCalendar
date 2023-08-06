#!/bin/sh

cd "$(dirname "$0")"
echo "Getting the weather"
python3 programs/parse_weather.py
sudo chmod 777 after-weather.svg
echo "Getting the details for the screen and making the text file"
python3 programs/parse_ical.py

echo "Converting the picture to PNG"
rsvg-convert --background-color=white -o almost_done.png almost_done.svg

echo "Optimising the picture for the kindle"
pngcrush -c 0 almost_done.png done.png

echo "Moving the picture to the server"
cp -f done.png /var/www/html/kindle/done.png
echo "Copying the text file"
mv -f Cal.txt /var/www/html/kindle/Cal.txt 
echo "All done!"
