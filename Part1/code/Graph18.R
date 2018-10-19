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

ggplot(length_df, aes(x=length)) + 
  geom_histogram(bins=30,aes(fill = ..count..)) + 
  geom_vline(aes(xintercept=mean(length)),
             color="#FFFFFF", linetype="dashed", size=1) +
  geom_density(aes(y=25 * ..count..),alpha=.2, fill="#1CCCC6") +
  ylab("Count") + xlab ("Length") + 
  ggtitle("Distribution of word count") + 
  theme_minimal()