import time
from bs4 import BeautifulSoup
import requests
def yahoo_news_auto_catch():
    
    url_list = []
    title_list = []

    main_url = 'https://baseball.yahoo.co.jp/npb/'
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    contents = soup.find(class_="io-pickup__itemTitle")
    title = contents.get_text()
    title = title.strip("\n")
    contents = contents.find("a")
    url = contents.get('href')
    
    url_list.append(url)
    title_list.append(title)
    print(title)
    print(url)
    
    for contents in soup.find_all(class_="io-list__itemArticleLink"):
    #contents = soup.find(class_="io-list__itemArticleLink")
        title = contents.get_text()
        title = title.strip("\n")
        title = title.strip("\u3000")
        url = contents.get('href')
        url_list.append(url)
        title_list.append(title)
        print(title)
        print(url)
    return url_list, title_list

import codecs
import pandas as pd

def Auto_tweet(coments, url, first_sentence):
    from requests_oauthlib import OAuth1Session
    import tweepy
    
    # TwitterAIPのトークン
    CK = 'mt8DhWrVIT95KRcY7CYaxOhuQ'
    CS = 'YLL2kbIXFLxx6k4IEbfyIvfw8vaVhJc034OZI5eiPSy3VydrAc'
    AT = '1318343582932111361-ydbazXnkKr7ESpWqNMIf7yh386HRYj'
    AS =  'ZgkjZ9A5UYf03ABCweVQJGlGqssiB9O6pKEbCVWfOtky8'
    
    # twotterオブジェクト
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT,AS)
    api = tweepy.API(auth)
    
    message = coments + "\n" + url + first_sentence
    # api.update_with_media(status = message, filename = file)
    api.update_status(status = message)

    print(message)
    
url_list, title_list = yahoo_news_auto_catch()

for coments, url in zip(title_list, url_list):
    main_url = url
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        
        contents = soup.find(class_="sc-jVODtj cJnPIe yjSlinkDirectlink")
        texts = contents.get_text()
        texts = texts.strip("\n")
        texts = texts.strip("\u3000")
        texts = texts.split("。")
        first_sentence = texts[0]
        print(first_sentence)
        first_sentence = "\n >>" + first_sentence

    except:
        print("Error")
        first_sentence = ""
    
    Auto_tweet(coments, url,first_sentence)
    time.sleep(120)