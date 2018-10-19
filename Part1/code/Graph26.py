# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:31:03 2018

@author: hongx
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
g = sns.boxenplot(x = year, y = week,
              color="b",
              scale="linear", data=dfnew1)
g.set(xlabel = "Years", ylabel = "Weeks")
g.set(title = "Comparison of the Weeks that Songs stayed on Board in Different Years")
plt.show()
