# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:32:01 2018

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

# Draw a heatmap with the numeric values in each cell
f, ax = plt.subplots(figsize=(9, 6))
g = sns.heatmap(heat)
g.set(xlabel = "Years", ylabel = "Months")
g.set(title = "Popularity of the Songs in different times")
plt.show()
