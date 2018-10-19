# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:26:17 2018

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
g = sns.jointplot(x11, x22, kind="kde", height=7, space=0)
#g.set(xlabel = "Relatively Time", ylabel = "Weeks")
#g.set(title = "Density of The Popularity of Songs in Years")
plt.title('Density of The Popularity of Songs in Years')
plt.show()