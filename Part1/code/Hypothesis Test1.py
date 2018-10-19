# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:42:23 2018

@author: hongx
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
import statsmodels.formula.api as sm1

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

linear_model = sm1.ols(formula='tweet_s ~ lyric_s + heat',data=set2)
results = linear_model.fit()
print(results.summary())
