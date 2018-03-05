# setup -------------------------------------------------------------------
library(tidyverse)
library(ggthemes)
library(lubridate)

df <- read_csv('./data/fake_news_clustered.csv')
topics <- read_csv('./data/fake_news_topic_key.csv')

topics_df <- df %>% 
  gather(topic_hier, topic, 22:24) %>% 
  select(-X1) %>% 
  mutate(topic_hier = substring(topic_hier,6,6)) %>% 
  left_join(topics, by = c('topic' ='topic_num')) %>% 
  select(-topic, -frequency, -X1) %>% 
  rename(topic = topic_name) %>% 
  filter(!is.na(topic))


# grab some text from a particular topic
gettopics <- function(name) {
  temp <- topics_df %>% 
    filter(topic == name) %>% 
    select(uuid, topic, topic_hier, text)
  
  return(temp)
}

natopicnums <- topics %>% filter(is.na(topic_name)) %>% pull(topic_num)


# Topic Frequency -----------------------------------------------------------
colnames(df) 

author_count <- df %>% 
  group_by(site_url) %>% 
  summarize(count = n()) %>% 
  arrange(desc(count))

df %>% filter(grepl('clickhole', site_url)) %>% select(title)

# topic frequency by site
site_topics <- topics_df %>% 
  group_by(site_url, topic) %>% 
  summarize(count = n()) %>% 
  arrange(desc(count)) %>% 
  filter(topic != 'spanish')

# overall topic frequency
topic_freq <- site_topics %>% 
  group_by(topic) %>% 
  summarize(count = sum(count)) %>% 
  arrange(desc(count))

top_topics = (arrange(topic_freq, desc(count)) %>% pull(topic))[1:13]

# overall topic numbers plot
ggplot(topic_freq) + 
  geom_col(aes(x = reorder(topic, count), y = count), fill = 'red3') +
  coord_flip() +
  labs(y = '# of Articles Published', x = '', 
       title = 'Full frequencies list',
       subtitle = 'Sorted by one-word summaries of each LDA-identified topic') +
  theme_few()

ggsave('./figures/overall_topic_freq.png', width = 6, height = 5)

# articles involving wikileaks
has_wikileaks <- df %>%
  select(uuid, topic1, topic2, topic3) %>% 
  mutate(about_wikileaks = ifelse(topic1 == 0 | topic2 == 0 | topic3 == 0, TRUE, FALSE)) %>% 
  mutate(about_wikileaks = factor(about_wikileaks,
                                  levels = c(TRUE, FALSE), 
                                  labels =c('Involves Wikileaks', 'Doesn\'t involve Wikileaks'))) %>% 
  mutate(could_classify = ifelse(topic1 %in% natopicnums, FALSE, TRUE)) %>% 
  mutate(could_classify = factor(could_classify,
                                 levels = c(TRUE, FALSE),
                                 labels = c('Classified', 'Not Classified')))


ggplot(has_wikileaks) +
  geom_bar(aes(x = could_classify, fill = about_wikileaks)) +
  labs(title = 'Wikileaks dominated the election',
       subtitle = 'Based on articles our LDA model succesfully classified',
       x = '', y = '# of Articles') +
  scale_fill_brewer(palette = 'Set1') +
  theme_few() +
  guides(fill = guide_legend(title = '', label.hjust = 2)) +
  theme(legend.position = 'bottom')

ggsave('./figures/has_wikileaks.png', width = 5, height = 7)

# Topics by Date -------------------------------------------------------------

topics_by_date <- topics_df %>%
  select(topic, published) %>% 
  filter(topic %in% top_topics) %>% 
  mutate(topic = factor(topic, levels = rev(top_topics))) %>% 
  filter(!(topic %in% c('canada', 'intelligence', 'gold'))) %>% 
  mutate(published = as_datetime(published))


ggplot(topics_by_date) +
  geom_jitter(aes(published, topic, color = topic), size = .7) +
  geom_vline(xintercept = as_datetime('2016-11-08'), color = 'blue3',
             size = 1) +
  scale_color_hue(direction = -1) +
  theme_few() +
  guides(color = FALSE) +
  labs(title = 'Wikileaks, Obamacare, and policing remain important after the election',
       subtitle = 'One dot represents one "fake news" article published about that topic',
       x = 'Date Published (2016)', y = '')
ggsave('./figures/topics_by_date.png', width = 12, height = 6)



# Sentiment Analysis ------------------------------------------------------
sentiment_df <- read_csv('./data/sentiment_scores.csv')

mentionsdf <- df %>% 
  select(uuid, text) %>% 
  mutate(just_clinton = grepl('clinton', tolower(text)) & !grepl('trump', tolower(text))) %>% 
  mutate(just_trump = !grepl('clinton', tolower(text)) & grepl('trump', tolower(text))) %>% 
  mutate(mention_both = grepl('clinton', tolower(text)) & grepl('trump', tolower(text))) %>% 
  mutate(no_mention = ifelse(!just_trump & !just_clinton & !mention_both, TRUE, FALSE)) %>% 
  select(-text) %>% 
  gather(mention_cat, val, 2:5) %>% 
  filter(val == TRUE) %>% 
  select(-val)

mentionssummary <- mentionsdf %>% 
  group_by(mention_cat) %>% 
  summarize(count = n()) %>% 
  ungroup()

ggplot(mentionssummary, aes(x = reorder(mention_cat, count), y = count)) + 
  geom_col(fill = 'red3') + 
  geom_text(aes(label = count), vjust = -.5)

article_sentiment <- mentionsdf %>% 
  left_join(sentiment_df, by = 'uuid')

