#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:28:19 2017

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
# Set random seed (for reproducibility)
np.random.seed(1000)

# Select whether using Keras with or without GPU support
# See: https://stackoverflow.com/questions/40690598/can-keras-with-tensorflow-backend-be-forced-to-use-cpu-or-gpu-at-will
use_gpu = False

config = tf.ConfigProto(intra_op_parallelism_threads=multiprocessing.cpu_count(), 
                        inter_op_parallelism_threads=multiprocessing.cpu_count(), 
                        allow_soft_placement=True, 
                        device_count = {'CPU' : 2, 
                                        'GPU' : 1 if use_gpu else 0})

session = tf.Session(config=config)
K.set_session(session)

dataset_location = './dataset.csv'
twitter_dataset_location = './Twitter_song_output_cleaned.csv'
model_location = './model/'

corpus = []
labels = []

with open(dataset_location, 'r', encoding='utf-8') as df:
    for i, line in enumerate(df):
        if i == 0:
            # Skip the header
            continue

        parts = line.strip().split(',')
        
        # Sentiment (0 = Negative, 1 = Positive)
        labels.append(int(parts[1].strip()))
        
        # Tweet
        tweet = parts[3].strip()
        if tweet.startswith('"'):
            tweet = tweet[1:]
        if tweet.endswith('"'):
            tweet = tweet[::-1]
        
        corpus.append(tweet.strip().lower())
        
print('Corpus size: {}'.format(len(corpus)))


### load twitter data
twitter_text = []
with open(twitter_dataset_location, 'r', encoding='utf-8') as twitter_df:
    for i, line in enumerate(twitter_df):
        if i == 0:
            # Skip the header
            continue

        parts = line.strip().split(',')
        
       
        
        # Tweet
        tweet = parts[6].strip()
        if tweet.startswith('"'):
            tweet = tweet[1:]
        if tweet.endswith('"'):
            tweet = tweet[::-1]
        
        twitter_text.append(tweet.strip().lower())
        
        
        
tkr = RegexpTokenizer('[a-zA-Z0-9@]+')
stemmer = LancasterStemmer()

tokenized_corpus = []
tokenized_twitter_corpus = []

for i, tweet in enumerate(corpus):
    tokens = [stemmer.stem(t) for t in tkr.tokenize(tweet) if not t.startswith('@')]
    tokenized_corpus.append(tokens)

for i, tweet in enumerate(twitter_text):
    tokens = [t for t in tkr.tokenize(tweet) if not t.startswith('@')]
    tokenized_twitter_corpus.append(tokens)
    
with open(model_location + 'tokenized_corpus.dill', 'wb') as f:
    dill.dump(tokenized_corpus, f)

with open(model_location + 'tokenized_twitter_corpus.dill', 'wb') as twitter_f:
    dill.dump(tokenized_twitter_corpus, twitter_f)
    
with open(model_location + 'tokenized_corpus.dill', 'rb') as f:
    tokenized_corpus = dill.load(f)

with open(model_location + 'tokenized_twitter_corpus.dill', 'rb') as twitter_f:
    tokenized_twitter_corpus = dill.load(twitter_f)

vector_size = 512
window_size = 10

# Create Word2Vec
word2vec = Word2Vec(sentences=tokenized_corpus,
                    size=vector_size, 
                    window=window_size, 
                    negative=20,
                    iter=50,
                    seed=1000,
                    workers=multiprocessing.cpu_count())

word2vec.save(model_location + 'word2vec.model')

word2vec = Word2Vec.load(model_location + 'word2vec.model')

X_vecs = word2vec.wv

# vectorize twitter data using Word2Vec
Twitter_word2vec = Word2Vec(sentences=tokenized_twitter_corpus,
                    size=vector_size, 
                    window=window_size, 
                    negative=20,
                    iter=50,
                    seed=1000,
                    workers=multiprocessing.cpu_count())

Twitter_word2vec.save(model_location + 'Twitter_word2vec.model')

Twitter_word2vec = Word2Vec.load(model_location + 'Twitter_word2vec.model')

Twitter_X_vecs = Twitter_word2vec.wv

Twitter_DF = pd.read_csv("Twitter_song_output_cleaned.csv" , sep=',', encoding='latin1')

del word2vec
del corpus

train_size = 1000000

test_size = 100000

avg_length = 0.0
max_length = 0

for tweet in tokenized_corpus:
    if len(tweet) > max_length:
        max_length = len(tweet)
    avg_length += float(len(tweet))
    
print('Average tweet length: {}'.format(avg_length / float(len(tokenized_corpus))))
print('Max tweet length: {}'.format(max_length))

max_tweet_length = 15
total_size = len(tokenized_corpus)
total_Twitter_size = len(tokenized_twitter_corpus)

# Generate random indexes
indexes = set(np.random.choice(len(tokenized_corpus), train_size + test_size, replace=False))

X_train = np.zeros((train_size, max_tweet_length, vector_size), dtype=K.floatx())
Y_train = np.zeros((train_size, 2), dtype=np.int32)
X_test = np.zeros((test_size, max_tweet_length, vector_size), dtype=K.floatx())
Y_test = np.zeros((test_size, 2), dtype=np.int32)

X_total = np.zeros((total_size, max_tweet_length, vector_size), dtype=K.floatx())
Y_total = np.zeros((total_size, 2), dtype=np.int32)

# create matrix to store all vectorized twitter data
X_twitter_total = np.zeros((total_Twitter_size, max_tweet_length, vector_size), dtype=K.floatx())
for i, index in enumerate(indexes):
    for t, token in enumerate(tokenized_corpus[index]):
        if t >= max_tweet_length:
            break
        
        if token not in X_vecs:
            continue
    
        if i < train_size:
            X_train[i, t, :] = X_vecs[token]
        else:
            X_test[i - train_size, t, :] = X_vecs[token]
            
    if i < train_size:
        Y_train[i, :] = [1.0, 0.0] if labels[index] == 0 else [0.0, 1.0]
    else:
        Y_test[i - train_size, :] = [1.0, 0.0] if labels[index] == 0 else [0.0, 1.0]

# take entire dataset as training dataset
for i in range(total_size):
    for t, token in enumerate(tokenized_corpus[i]):
        if t >= max_tweet_length:
            break
        
        if token not in X_vecs:
            continue
        X_total[i, t, :] = X_vecs[token]
        Y_total[i, :] = [1.0, 0.0] if labels[i] == 0 else [0.0, 1.0]
        
# try to predict on entire twitter dataset we have
for i in range(total_Twitter_size):
    for t, token in enumerate(tokenized_twitter_corpus[i]):
        
        if t >= max_tweet_length:
            break
        
        if token not in Twitter_X_vecs:
            continue
        X_twitter_total[i, t, :] = Twitter_X_vecs[token]
        

batch_size = 64
nb_epochs = 1

model = Sequential()

model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same', input_shape=(max_tweet_length, vector_size)))
model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same'))
model.add(Dropout(0.25))


model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(256, activation='tanh'))
model.add(Dense(256, activation='tanh'))
model.add(Dropout(0.5))

model.add(Dense(2, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=0.0001, decay=1e-6),
              metrics=['accuracy'])

# Fit the model
h = model.fit(X_train, Y_train,
          batch_size=batch_size,
          shuffle=True,
          epochs=nb_epochs,
          
          callbacks=[EarlyStopping(min_delta=0.00025, patience=2)])

predicted_Twitter_sentiment = pd.DataFrame(model.predict(X_twitter_total))
predicted_Twitter_sentiment.loc[:, 'score'] = np.zeros(len(predicted_Twitter_sentiment))

for i in range(len(predicted_Twitter_sentiment)):
    if predicted_Twitter_sentiment.loc[i, 0] > predicted_Twitter_sentiment.loc[i, 1]:
        predicted_Twitter_sentiment.loc[i, 'score'] = 0
    else:
        predicted_Twitter_sentiment.loc[i, 'score'] = 1
model.save('Twitter_train_model.h5')
model = load_model('Twitter_train_model.h5')

outputFileName = "Twitter_sentiment_score.csv"    
with open(outputFileName, 'w') as output:  
    predicted_Twitter_sentiment.to_csv(output, sep = ',')
output.close()

Twitter_DF_cleaned = pd.read_csv("Twitter_song_output_cleaned.csv" , sep=',', encoding='latin1')
Twitter_final = pd.concat([Twitter_DF_cleaned, predicted_Twitter_sentiment], axis = 1)

outputFileName = "Twitter_data_with_sentiment_score.csv"    
with open(outputFileName, 'w') as output:  
    Twitter_final.to_csv(output, sep = ',')
output.close()

regex2=re.compile('!') 

# regular expression to find link in text attribute
sentiment = 0
row_count = 0

for i in Twitter_final.index:
    text = Twitter_final.ix[i, "text"]
    if bool(re.search(regex2, str(text))):
        #print(text)
        row_count += 1
        sentiment += Twitter_final.loc[i, 'score']
mean_sentiment = sentiment / row_count

#plot the histogram of sentiment score frequency distribution
plt.figure(figsize = [8, 8])
bar_colors= ['r', 'b']
plt.bar(x = ['0', '1'], height = [len(Twitter_final[Twitter_final['score']==0]), len(Twitter_final[Twitter_final['score']==1])], color = bar_colors, width=0.5, bottom=None,  align='center', data=None)
plt.ylabel(s = 'frequency')
plt.xlabel(s = 'sentiment score')
plt.title(s = 'frequency of sentiment score')
plt.savefig('frequency_sentiment_score.png')