# Simple bag-of-words search
This repository contains simple implementation of the bag-of-words search algorithm.

## Quick Setup (shell)

```shell script
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
After running the `flask run` command the preprocessing of the articles is started.

You can adjust [the config file](https://github.com/maciektr/BagOfWordsSearch/blob/master/config.py) with the crawler source of your liking.

## Application design

### UI
The search engine is exposed to user through a simple flask app.

![Front end design](https://github.com/maciektr/BagOfWordsSearch/blob/master/docs/img/ui1.png)

The search results are returned as a list of articles recognized as the closest match.

![Front end design](https://github.com/maciektr/BagOfWordsSearch/blob/master/docs/img/ui2.png)

### Test pages
The search engine is tested against the articles from English Wikipedia. The articles are obtained for preprocessing with a simple crawler implemented in [gather_pages file](https://github.com/maciektr/BagOfWordsSearch/blob/master/preprocessing/gather_pages.py), which downloads all documents linked on a page given in [config](https://github.com/maciektr/BagOfWordsSearch/blob/daab9a1c88bc3841577df3fa6e100de5fb78fd1d/config.py#L15). Then they are parsed, cleaned, stepped and represented as [tf-idf vectors](https://pl.wikipedia.org/wiki/TFIDF) (all implemented in [preprocessing folder](https://github.com/maciektr/BagOfWordsSearch/tree/master/preprocessing)).
