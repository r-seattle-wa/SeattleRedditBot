#!/bin/bash

path=/opt/reddit/SeattleRedditBot
daily_base_text=$path/daily-post.body.base
daily_weather_file=$path/today-weather.txt
daily_footer=$path/daily-post.body.footer
final_file=$path/daily-post.txt



# Build the daily self.post 
# daily-post.body.base is the core text to edit
cat $daily_base_text > $final_file

# add in the weather
cat $daily_weather_file >> $final_file

# add in the footer
cat $daily_footer >> $final_file

cat $final_file
