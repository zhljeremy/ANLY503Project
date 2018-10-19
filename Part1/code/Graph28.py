# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:33:40 2018

@author: hongx
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

music = pd.read_csv("music_lyrics.csv")
#music.head()
d11 = music["date"]
music["right_date"] = pd.to_datetime(d11)

dfnew1 = pd.DataFrame()
dfnew1["Relatively Time"] = music["right_date"]
dfnew1["Weeks"] = music['total weeks']
dfnew1 = dfnew1.groupby("Relatively Time").sum()
x11 = dfnew1.index
x22 = dfnew1["Weeks"]

test = pd.read_csv("Twitter_data_with_sentiment_score.csv")
d = test["date"]
test["juest_date"] = pd.to_datetime(d)
d2 = test["juest_date"]
test["final_date"] = d2.dt.date
test["hot"] = test.retweets + test.favorites
dfnew1 = pd.DataFrame()
dfnew1["date"] = test["final_date"]
dfnew1["retweets"] = test["retweets"]
dfnew1["favorites"] = test["favorites"]
dfnew1 = dfnew1.groupby("date").sum()

music = pd.read_csv("lyrics_sentiment_no_lyrics.csv")
#music.head()
d11 = music["date"]
music["right_date"] = pd.to_datetime(d11)
music["year"] = music["right_date"].map(lambda x: x.year)

dfnew1 = pd.DataFrame()
dfnew1["date"] = music["year"]
dfnew1["count"] = music['total weeks']
sns.set(style="whitegrid")
year = dfnew1["date"]
week = dfnew1["count"]

music = pd.read_csv("music_lyrics.csv")
#music.head()
d11 = music["date"]
music["right_date"] = pd.to_datetime(d11)
dfnew1 = pd.DataFrame()
dfnew1["date"] = music["right_date"]
dfnew1["count"] = music['total weeks']
dfnew1["count1"] = dfnew1["count"].groupby(dfnew1["date"]).transform("sum")
dfnew1 = dfnew1.drop_duplicates(subset='date', keep="last")
dfnew1["year"] = dfnew1["date"].map(lambda x: x.year)
dfnew1["month"] = dfnew1["date"].map(lambda x: x.month)
from datetime import datetime
dfnew1["month1"] = dfnew1["date"].map(lambda x: datetime.strptime(str(x.month), '%m').strftime('%B'))
#dfnew1["count2"] = dfnew1["count1"].groupby(dfnew1["year", "month"]).transform("sum")
dfnew1["count2"] = dfnew1.groupby(['year','month1']).count1.transform('sum')
dfnew1 = dfnew1.drop_duplicates(subset=['year', 'month1'], keep = "last")
dfnew1["count2"] = dfnew1["count2"].astype(int)
dfnew1["year"] = dfnew1["year"].astype(int)
heat = dfnew1.pivot("month1", "year", "count2")

test1 = pd.read_csv("Twitter_data_with_sentiment_score.csv")
d = test1["date"]
test1["juest_date"] = pd.to_datetime(d)
d2 = test1["juest_date"]
test1["final_date"] = d2.dt.date
#point = np.random.uniform(0, 1, size= len(test1.username))
test1["point"] = test1["score"]
test1["finalpoint"] = test1.groupby(['song and artist']).point.transform(np.mean)
test1 = test1.drop_duplicates(subset='song and artist', keep="last")
test2 = pd.read_csv("lyrics_sentiment_no_lyrics.csv")
#dfnew1["count2"] = dfnew1.groupby(['year','month1']).count1.transform()
test2['artists'] = ' ' + test2['artists']
test2['song and artist'] = test2['title'] + test2['artists']
set1 = pd.DataFrame()
set1 = pd.merge(test1, test2, on='song and artist')
set2 = pd.DataFrame()
set2['tweet_s'] = set1['finalpoint']
set2['lyric_s'] = set1['Sentiment']
set2['heat'] = set1['total weeks']

g = sns.relplot(x='tweet_s', y='lyric_s', size='heat', data = set2)
g.set(xlabel = "Sentiment Analysis results for Tweets", ylabel = "Sentiment Analysis results for Lyrics")
g.set(title = "Relationship between the Sentiment Analysis Results from Tweets and Lyrics")
plt.show()