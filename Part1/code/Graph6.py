#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:32:11 2018

@author: Tianjing Cai
"""
import sys
import matplotlib.pyplot as plt

# Read Twitter cleaning statistics
Twitter_stat = []
inputFileName = "Twitter_cleaning_count.txt" 
with open(inputFileName, 'r') as Input:
    Twitter_stat = Input.readlines()
Input.close()

Twitter_DF_length = int(Twitter_stat[0])
irrelevant_content = int(Twitter_stat[1])
duplicate_count = int(Twitter_stat[2])
link_in_text = int(Twitter_stat[3])

#plot the histogram
plt.figure(figsize = [8, 8])
bar_colors= ['r', 'b', 'g', 'm']
plt.bar(x = ['total \ntwitter data', 'irrelevant \ncontent in text', 'duplicate \npost', 'link in \ntext'], height = [Twitter_DF_length/Twitter_DF_length* 100, (irrelevant_content)/Twitter_DF_length*100, duplicate_count/Twitter_DF_length*100, link_in_text /Twitter_DF_length*100], color = bar_colors, width=0.8, bottom=None,  align='center', data=None)
plt.ylabel(s = 'percentage of data')
plt.xlabel(s = 'data type')
plt.title(s = 'Types of data when doing data cleaning')
plt.savefig('Twitter_cleaning_category.png')
