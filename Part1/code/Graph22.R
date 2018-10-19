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

lyrics_text <- lyrics$lyric
#Removing punctations and alphanumeric content
lyrics_text<- gsub('[[:punct:]]+', '', lyrics_text)
lyrics_text<- gsub("([[:alpha:]])\1+", "", lyrics_text)

# Getting the sentiment value for the lyrics
ty_sentiment <- get_nrc_sentiment((lyrics_text))

# Dataframe with cumulative value of the sentiments
sentimentscores<-data.frame(colSums(ty_sentiment[,]))

# Dataframe with sentiment and score as columns
names(sentimentscores) <- "Score"
sentimentscores <- cbind("sentiment"=rownames(sentimentscores),sentimentscores)
rownames(sentimentscores) <- NULL

lyrics$lyric <- as.character(lyrics$lyric)

tidy_lyrics <- lyrics %>% 
  unnest_tokens(word,lyric)

song_wrd_count <- tidy_lyrics %>% count(track_title)

lyric_counts <- tidy_lyrics %>%
  left_join(song_wrd_count, by = "track_title") %>% 
  rename(total_words=n)

lyric_sentiment <- tidy_lyrics %>% 
  inner_join(get_sentiments("nrc"),by="word")

lyric_sentiment %>% 
  count(word,sentiment,sort=TRUE) %>% 
  group_by(sentiment)%>%top_n(n=10) %>% 
  ungroup() %>%
  ggplot(aes(x=reorder(word,n),y=n,fill=sentiment)) +
  geom_col(show.legend = FALSE) + 
  facet_wrap(~sentiment,scales="free") +
  xlab("Sentiments") + ylab("Scores")+
  ggtitle("Top words used to express emotions and sentiments") +
  coord_flip()