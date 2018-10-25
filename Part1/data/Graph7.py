"""
@author: Tianjing Cai
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import dill
import keras
import keras.backend as K
import multiprocessing
import tensorflow as tf
import numpy as np
import pandas as pd
from gensim.models.word2vec import Word2Vec

from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv1D
from keras.optimizers import Adam

from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
from keras.models import load_model
import re




# Read Twitter cleaning statistics
Twitter_sentiment = []
inputFileName = "Twitter_sentiment_stat.txt" 
with open(inputFileName, 'r') as Input:
    Twitter_sentiment = Input.readlines()
Input.close()

negative_sentiment_count = int(Twitter_sentiment[0])
positive_sentiment_count = int(Twitter_sentiment[1])


#plot the histogram of sentiment score frequency distribution
plt.figure(figsize = [8, 8])
bar_colors= ['r', 'b']
plt.bar(x = ['0', '1'], height = [len(Twitter_final[Twitter_final['score']==0]), len(Twitter_final[Twitter_final['score']==1])], color = bar_colors, width=0.5, bottom=None,  align='center', data=None)
plt.bar(x = ['0', '1'], height = [negative_sentiment_count, positive_sentiment_count], color = bar_colors, width=0.5, bottom=None,  align='center', data=None)
plt.ylabel(s = 'frequency')
plt.xlabel(s = 'sentiment score')
plt.title(s = 'frequency of sentiment score')
plt.savefig('frequency_sentiment_score.png')