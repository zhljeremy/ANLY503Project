#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:48:52 2017

@author: Tianjing Cai

This program read dirty twitter Data and fix incorrect values and remove duplicate rows
Also this program generate a cleanliness score that report how clean current data is after
implementing several cleaning methods and then output dataset to csv file
"""
import sys
import pandas as pd
import csv
import re
import nltk
import matplotlib.pyplot as plt
Twitter_DF = pd.read_csv("Twitter_song_dirty.csv" , sep=',', encoding='utf8')

# regular expression to match key words in text attribute




# regular expression of all those non-alphabetic/number/space    
regex2=re.compile('[^A-Za-z0-9\s\d\.]+') 

# regular expression to find link in text attribute
regex3= re.compile('https.+$ | http.+$|pic\.twitter\.com.*$') 
id_link = {}
irre_count = 0
dirty_count = 0 # count number of that has dirty value in attribute "text"
link_in_text = 0
irrelevant_content = 0
duplicate_count = 0
format_wrong = 0
dirty_index = [] # store index of duplicate rows
irrelevant_content_store = []
print("Begin to find incorrect / missing values from dataframe: ")
for i in Twitter_DF.index:
    person_link = Twitter_DF.ix[i, "permalink"]
    
    ID = Twitter_DF.ix[i, "id"]
    # check number of digits for each id
    if( not len(str(ID)) == 18):
        
        format_wrong = format_wrong +1
    
    text = Twitter_DF.ix[i, "text"]
    
    # remove link in text
    if bool(re.search(regex3, str(text))):
        link_in_text = link_in_text  +1
        
        Twitter_DF.ix[i, "text"] = re.sub(regex3, "", str(Twitter_DF.ix[i, "text"])) 
    
    # clean text data: remove those non alphabetic symbol / digits/ space and dot
    if bool(re.search(regex2, str(text))):
        irrelevant_content = irrelevant_content +1
        dirty_text = re.search(regex2, str(text))[0]
        #print(dirty_text)
        irrelevant_content_store.append(dirty_text)
        Twitter_DF.ix[i, "text"] = re.sub(regex2, "", str(Twitter_DF.ix[i, "text"])) 
    
    # store row indices that does not contain relevant keywords
    
    
    # store row indices that has duplicate twitter post
    if ID in id_link.keys() and id_link[ID] == Twitter_DF.ix[i, "permalink"]:
        duplicate_count = duplicate_count +1
        dirty_index.append(i)
    
    # store post id and its link 
    else:
        id_link[ID] = Twitter_DF.ix[i, "permalink"]



      
final_clean_percent = len(Twitter_DF.index) - irre_count - dirty_count - duplicate_count - format_wrong
first_clean_percent = len(Twitter_DF.index) - dirty_count - format_wrong
second_clean_percent = len(Twitter_DF.index) - dirty_count - duplicate_count - format_wrong
third_clean_pencent = len(Twitter_DF.index) - dirty_count - duplicate_count - irre_count - format_wrong

print("After removing dirty value, dirty score", str(final_clean_percent/first_clean_percent))
print("After removing number of duplicate rows, dirty score: ", str(final_clean_percent/second_clean_percent))
print("After removing number of rows that has irrelavant information, dirty score:  ", str(final_clean_percent/third_clean_pencent))

print("Begin drop duplicate rows: ")
for index in dirty_index:
    
    Twitter_DF.drop(index)
    
   #word_list = nltk.Text(all_word)
#word_list.findall(r"<[Ii][Pp][Hh][Oo][Nn][Ee]><is>(<.*>)") 
print("output our dataframe: ")
outputFileName = "Twitter_song_output_cleaned2.csv"    
with open(outputFileName, 'w') as output:  
    Twitter_DF.to_csv(output, sep = ',')
output.close()

fdist = nltk.FreqDist(irrelevant_content_store) 
def plot_freq_words(fdist):
    df = pd.DataFrame(columns=('non-alphabetic-symbols', 'freq'))
    i = 0
    for word, frequency in fdist.most_common(21):
        df.loc[i] = (word, frequency)
        i += 1

    title = 'Top %s non-alphabetic characters in tweets' % top_n
    
    ax = df.plot
    
    barh = ax.barh(x='non-alphabetic-symbols', y='freq', title=title, figsize=(8,8)).invert_yaxis()
    #fig = barh.get_figure()
    fig = plt.gcf()
    fig.savefig('Top_20_non_alphabetic_tweets.png')
    #barh.savefig('Top %s non-alphabetic characters in tweets' )
    
    #fig.savefig('Top %s non-alphabetic characters in tweets.png')
    
    return
    
top_n = 20
#text.dispersion_plot([str(w) for w, f in fdist.most_common(top_n)])
plot_freq_words(fdist)

outputFileName = "Twitter_cleaning_count.txt"    
with open(outputFileName, 'w') as output:  
    output.write(str(len(Twitter_DF)) + '\n')
    
    output.write(str(irrelevant_content)+ '\n')
    output.write(str(duplicate_count)+ '\n')
    output.write(str(link_in_text))
output.close()


