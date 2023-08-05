#!/bin/sh

cd "$(dirname "$0")"
echo "Getting the weather"
python3 programs/parse_weather.py
sudo chmod 777 after-weather.svg
echo "Getting the details for the screen"
python3 programs/parse_ical.py
echo "Converting the picture"
rsvg-convert --background-color=white -o almost_done.png almost_done.svg
echo "Optimising the picture for the kindle"
#We optimize the image
pngcrush -c 0 almost_done.png done.png

#We move the image where it needs to be
#rm /var/www/html/kindle/done.png
echo "Moving the picture to the server"
cp -f done.png /var/www/html/kindle/done.png
echo "Making the text file"
python3 programs/make_txt.py
echo "Copying th etext file"
mv -f Cal.txt /var/www/html/kindle/Cal.txt 
echo "All done!"
#rm basic.ics
#rm after-weather.svg
#rm almost_done.png
#rm almost_done.svg

