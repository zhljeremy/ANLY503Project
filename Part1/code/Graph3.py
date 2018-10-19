# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 21:54:07 2018

@author: hongx
"""

import pandas as pd
from langdetect import detect, DetectorFactory
import matplotlib.pyplot as plotter
from collections import Counter

df = pd.read_csv("music_lyrics.csv")
df.drop(df.columns[[0, 1]], axis=1, inplace = True)
df1 = df.dropna()
mydf = df1[df1.lyrics != 'No Lyrics']

DetectorFactory.seed = 0
lang = []
for i in list(set(mydf.lyrics)):
    lang.append(detect(i))


Counter(lang)
pieLabels = 'en', 'es', 'tl', 'ko', 'so', 'cy', 'pt'
numofsongs = [3982, 29, 1, 2, 1, 2, 2]
figureObject, axesObject = plotter.subplots()
explodeTuple = (0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
axesObject.pie(numofsongs, explode=explodeTuple,

        labels=pieLabels,

        autopct='%1.2f',

        startangle=90)
plotter.title("Pie chart for lyric languages " + "(2008 - 2018)")
axesObject.axis('equal')

pieLabels = 'es', 'tl', 'ko', 'so', 'cy', 'pt'
numofsongs = [29, 1, 2, 1, 2, 2]
figureObject, axesObject = plotter.subplots()
axesObject.pie(numofsongs,labels=pieLabels, autopct='%1.2f', startangle=90)

axesObject.axis('equal')
plotter.title(
    "Pie chart for lyric languages without English " + "(2008 - 2018)")
plotter.show()