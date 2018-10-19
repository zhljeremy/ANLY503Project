# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 21:54:07 2018

@author: hongx
"""

##Python Code
from os import path
from PIL import Image
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

def define_stopwords():
  set(stopwords.words('english'))
  
  st1 = ["ain't","I'm","after","afterwards","again","against","all","almost",
         "alone","along","already","also","although","always","am","among",
         "amongst","amoungst","amount","an","and","another","any","anyhow",
         "anyone","anything","anyway","anywhere","are","around","as","at","back",
         "be","became","because","become","becomes","becoming","been","before",
         "beforehand","behind","being","below","beside","besides","between",
         "beyond","bill","both","bottom","but","by","call","can\'t","can",
         "cannot","cant","co","con","cause","could","couldnt","cry","de",
         "describe","detail","do","done","down","due","during","each","eg",
         "eight","either","eleven","else","elsewhere","empty","enough","etc",
         "even","ever","every","everyone","everything","everywhere","except",
         "few","fifteen","fifty","fill","find","fire","first","five","for",
         "former","formerly","forty","found","four","from","front","full",
         "further","get","got","give","go","had","has","hasnt","have","he",
         "hence","her","here","hereafter","hereby","herein","hereupon","hers",
         "herself","him","himself","his","how","however","hundred","i","ie","if",
         "in","inc","indeed","interest","into","is","it","its","itself","keep",
         "last","latter","latterly","least","less","ltd","made","many","may",
         "me","meanwhile","might","mill","mine","more","moreover","most",
         "mostly","move","much","must","my","myself","name","namely","neither",
         "never","nevertheless","next","nine","no","nobody","none","noone","nor",
         "not","nothing","now","nowhere","of","off","often","oh","on","once",
         "one","only","onto","or","other","others","otherwise","our","ours",
         "ourselves","out","over","own","part","per","perhaps","please","put",
         "rather","re","same","see","seem","seemed","seeming","seems","serious",
         "several","she","should","show","side","since","sincere","six","sixty",
         "so","some","somehow","someone","something","sometime","sometimes",
         "somewhere","still","such","system","take","ten","than","that","the",
         "their","them","themselves","then","thence","there","thereafter",
         "thereby","therefore","therein","thereupon","these","they","thick",
         "thin","third","this","those","though","three","through","throughout",
         "thru","thus","to","together","too","top","toward","towards","twelve",
         "twenty","two","un","under","until","up","upon","us","very","via","was",
         "we","well","were","what","whatever","when","whence","whenever","where",
         "whereafter","whereas","whereby","wherein","whereupon","wherever",
         "whether","which","while","whither","who","whoever","whole","whom",
         "whose","why","will","with","within","without","would","yet","you",
         "yeah","your","yours","yourself","yourselves"]

  
  stop_words = stopwords.words('english')
  stop_words.extend(
      ['from', 'subject', 're', 'edu', 'use','a','about', 'above', 'across']
      +st1)
  return stop_words

def collect_text(top = None):
  lyrics_df = pd.read_csv("./music_lyrics.csv", index_col = 0)

  lyrics_df.lyrics = [
      'No Lyrics' if type(x) == float else x for x in lyrics_df.lyrics]
  
  if top != None:
    lyrics_df = lyrics_df[lyrics_df['peak'] <= top]

  text = " ".join(lyric for lyric in list(set(lyrics_df.lyrics)))
  print(
      "There are {} words in the combination of all review.".format(len(text)))
  
  return text

def transform_format(val):
    if val == 0:
        return 255
    else:
        return val

def creat_mask(image_path):
  music_coloring = np.array(Image.open(image_path))
        
  transformed_music_coloring = np.ndarray((
      music_coloring.shape[0],music_coloring.shape[1]), np.int32)
  
  for i in range(len(music_coloring)):
      transformed_music_coloring[i] = list(
          map(transform_format, music_coloring[i]))
    
  return transformed_music_coloring

def grey_color_func(
    word, font_size, position,orientation,random_state=42, **kwargs):
    return("hsl(230,100%%, %d%%)" % np.random.randint(0, 100))

# Generate a word cloud image
def generate_wordcloud(text, stop_words, coloring, output_path):
  wordcloud = WordCloud(
      stopwords=stop_words, mask=transformed_music_coloring, 
      background_color="white").generate(text)
  
  wordcloud.recolor(color_func = grey_color_func)
  
  my_dpi = 300
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  plt.savefig(output_path, format="png", dpi=my_dpi)

stop_words = define_stopwords()
text = collect_text(100)
transformed_music_coloring = creat_mask("./86932.png")
generate_wordcloud(
    text, stop_words, transformed_music_coloring, "music_wordcloud_top5.png")