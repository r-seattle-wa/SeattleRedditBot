
#!/bin/bash

path=/root/reddit/daily-post
file=today-weather.txt


# get our forecast from the NWS
curl -sL "http://forecast.weather.gov/MapClick.php?lat=47.62&lon=-122.36&unit=0&lg=english&FcstType=text&TextType=1" | html2text > $path/today-pre.txt

# forecast txt header
echo > $path/$file
echo "**Weather forecast for the /r/SeattleWA metro area from the NWS as of:** `date "+%m/%d/%y, %r"`" >> $path/$file
echo >> $path/$file
cat $path/today-pre.txt | echo -n `sed 's/^$/STARTPARA/'`|sed 's/STARTPARA/\n\n/g'|grep -Ev "=============|47.62°N|http://www.wrh.noaa.gov/sew"|sed -e 'G;G;'|sed -E s/":"/": "/g |grep -v -i "overnight:"|grep -a [a-z]|sed -e 's/^/*/' | grep -v -E "Short_Term_Forecast|Tonight: "| head -3 | grep [a-z]  >> $path/$file

# rm tmp file
#rm -f $path/today-pre.txt

cat $path/$file
