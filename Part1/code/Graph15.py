# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:12:43 2018

@author: hongx
"""

##Python Code
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import numpy as np

df = pd.read_csv('top20.csv')
count = df['count']
y_pos = np.arange(len((df.artist)))
plt.bar(y_pos, count)
plt.tick_params(axis = 'both', which = 'major', labelsize = 5)
plt.xticks(y_pos, (df.artist), rotation=20)
plt.xlabel('Artists')
plt.ylabel('Count in Billboard')
plt.title("Bar Chart for Singers' Songs in Billboard")
#plt.figure(figsize=(1000,1000))
plt.savefig('top20count.jpg', format="jpg", dpi = 500)