# setup -------------------------------------------------------------------
library(tidyverse)


# First Section -----------------------------------------------------------
df <- read_csv('./data/fake_news_clustered.csv')
topics <- read_csv('./data/fake_news_topic_key.csv')

colnames(df)

author_count <- df %>% 
  group_by(site_url) %>% 
  summarize(count = n()) %>% 
  arrange(desc(count))

df %>% filter(grepl('clickhole', site_url)) %>% select(title)
                                                       