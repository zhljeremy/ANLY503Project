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

#adding year column by matching track_title
length_df$year <- lyrics$year[match(length_df$track_title, lyrics$track_title)] 

length_df %>% 
  group_by(year) %>% 
  summarise(length = mean(length)) %>%
  ggplot(., aes(x= factor(year), y=length, group = 1)) +
  geom_line(colour="#1CCCC6", size=1) + 
  ylab("Average word count") + xlab ("Year") + 
  ggtitle("Year-wise average Word count change") + 
  theme_minimal() 