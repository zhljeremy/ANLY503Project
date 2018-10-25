#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 14:25:03 2018

@author: Tianjing Cai
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 11:35:35 2017

@author: Tianjing Cai
This program use GotOldTweets package to find all twitters that sent past 7 days,
and we could use query to grab data online and we output all those dataset to csv file.
"""


import sys
import got3
import pandas as pd
import csv
import re
from datetime import datetime
from dateutil.parser import parse
from datetime import date, timedelta
# Scraped twitter using API package called "old_tweet"
import ast



dictionary = {}
with open("chart_top10.txt", "r") as data:
    dictionary = ast.literal_eval(data.read())

print('open csv file: ')
outputFileName = "Twitter_song_dirty.csv"

output = open(outputFileName, 'w')
writer = csv.writer(output)
# write header to file
writer.writerow(["song and artist", "username", "date", "retweets", "favorites", "text", "geo", "mentions", "hashtags", "id", "permalink"])
output.close()




output = open(outputFileName, 'a')
writer = csv.writer(output)

                # January 1st
#d += timedelta(days = 6 - d.weekday())  # First Sunday

#song_date_store =

for artist_song, d_begin in dictionary.items():
# create month-date pair that we want to grab information at
    artist_song = artist_song.replace('+', ' ')

    
    print('Begin to gather data from twitter and write to csv file: ')
    
    for i in list(range(0, 7)):
        Start_YEAR_MONTH_DATE = parse(d_begin)
        End_YEAR_MONTH_DATE = Start_YEAR_MONTH_DATE + timedelta(days = i)
        # set tweeter search criteria: english only, 1000 tweets maximum per day, and time range given
        tweetCriteria = got3.manager.TweetCriteria().setQuerySearch(artist_song).setLang('en').setSince(str(Start_YEAR_MONTH_DATE)[0:10]).setUntil(str(End_YEAR_MONTH_DATE)[0:10]).setMaxTweets(30)
        # get information that store all tweets
        tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
        

        for t in tweets:
            if not(t is None):
                # write each tweet to csv file
                #print([artist_song, t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink])
                writer.writerow([artist_song, t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink])
output.close()


