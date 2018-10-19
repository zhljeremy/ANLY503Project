library(magrittr)
library(stringr)
library(dplyr)
library(ggplot2)
library(tm)
library(wordcloud)
library(syuzhet)
library(tidytext)
library(tidyr)
library(igraph)
library(ggraph)
library(readr)
library(circlize)
library(reshape2)

lyrics <- read.csv('taylor_swift_lyrics.csv')

lyrics$length <- str_count(lyrics$lyric,"\\S+") 

length_df <- lyrics %>% 
  group_by(track_title) %>% 
  summarise(length = sum(length))

length_df %>% 
  arrange(length) %>%
  slice(1:10)

lyrics %>% 
  group_by(track_title,year, album) %>% 
  summarise(length = sum(length)) -> length_df_track

ggplot(length_df_track, aes(x=reorder(album, year), y=length, fill=album))+
  geom_boxplot()+xlab("Count")+ylab("Album")+
  ggtitle("Boxplot for Album-wise Word Count")