# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 22:49:19 2018

@author: hongx
"""

from matplotlib import pylab
import matplotlib.pyplot as plt

def plot_freq_words(fdist):
    df = pd.DataFrame(columns=('word', 'freq'))
    i = 0
    for word, frequency in fdist.most_common(21):
        df.loc[i] = (word, frequency)
        i += 1

    title = 'Top %s words in lyrics' % top_n
    df.plot.barh(x='word', y='freq', title=title, figsize=(5,5)).invert_yaxis()
    
    return
    
top_n = 20

plot_freq_words(fdist)