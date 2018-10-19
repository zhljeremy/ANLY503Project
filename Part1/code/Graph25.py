# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:27:01 2018

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
g = sns.lineplot(data=dfnew1)
g.set(xlabel = "Years", ylabel = "Count Numbers")
g.set(title = "People Reactions for the Songs on Tweeter in Years")
plt.show()