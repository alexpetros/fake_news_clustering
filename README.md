## Fake News Topic Clustering 
#### About 
QSS 30.02 final project, which aims to classify large groups of fake news by topic, and perform analysis on the origin and impact of articles broken down by those topics. 

Written by Nidhi Rao, Colin Boit, Randy Zhang, and Alex Petros

### Build instructions

#### Requirements
Requires the `fake_news.json` file, which is too large to upload to github. 

In order to save time, the program will first check for pre-existing `pickles/*.pkl` files (which I have uploaded), and if the necessary files aren't present, then it will create the model from scratch using `data/fake_news.json`. The program expects those directories to be present, so they have been included in the git even though at the moment they are empty.

#### Build
Clone the repo with:

`git clone https://github.com/alexpetros/fake_news_clustering.git`

`cd fake_news_clustering/`

Now you're in the project root director. To build the files and run the preliminary sorting, use the following two commands:

`chmod +wrx analyze.py`

`./analyze.py`

This will build the `.pkl` files if you decided to make your own (requires json file), and then save the artice and topics `.csv` files in the root directory. Shouldn't take more than a few minutes.


#### What it does
Right now we've built two dataframes. The  first is a key where the topic numbers correspond to topic names. Since the algoirthm is not deterministic, it's possible that if you don't use our `.pkl`  file your topics won't match up with ours. However we've left them in the demonstrate the process.

The second dataframe contains one row for each article, and and all the json information about the article, in addition to three columns that contain the 3 most significant topics for that article. The toppics are stored as numbers which correspond to the topic numbers in the key dataframe. If the model identified only 2 or fewer topics for a given document, then the remaining slots contain -1. 