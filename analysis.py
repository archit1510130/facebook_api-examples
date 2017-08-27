import facebook
import requests
import pandas as pd
from pandas.io.json import json_normalize
import json
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

access_token="EAACEdEose0cBACAir6FVDZCQZBwBpggNn4F1iRcS2CMODGCugidMOvvUQJHJoHLZClGmovmCusgzdUwF8F8uX1RZAMS68o2iNhHOgSoP359RGuwfw7T6Wn9NZBbjNLSqevIweoiMOGsNuTC1RIQXOjAjRSarG2RCEbCN6HQkHZCWLbeBtkLlmaYNOEzZBvqPrJnl3luIx3cVx2hOFKPXXhxeKc5IEnz5EkZD"
#access_token="EAACEdEose0cBAErKPkETBAG2NJvqZC4LxUBvKPRgMxG8CZC6E0N90enykfH80Cs51axGGDYI7aT4qjtFUweZC3xCM6Pa64bQFM62JxCub2rRAobXv9vZAQ1MQK6PrPVYcZANcWrL0A4faia0gYg5hEGEm9QXTomTNml1M8sYRjmP5LGs0wDsPmZBi8Yls6XIyKtAwoj2ZCochAg3AgKOxBzWHNkgMSy12wZD"
#access_token="EAACEdEose0cBAIqPxlp4jzImRMZAKnK9Ul6LlnM0GoErdsMxo4zYu8cx6wdnGkZADR1PZCZBDXfKsUln2Y3GeHM7UFvi5ZAm3ZCj1hfnnD6mZBvOe06vh4dUsxDQUKZAgLSrLX6S4fKHEXa3MO3XsyLTxUm2hq1zkIvokEdzkm4GrpzZBDFSjkg5D7gw1PKPZAkJu6IRocogrQZCxHhLkKGlHYZBuMu3juhwDI2T03a9msjWqjTlxEZA6OPHZB4THFL1HA3pIZD"
graph = facebook.GraphAPI(access_token=access_token, version='2.5')
fields=['name','id','email','education','friends','age_range','birthday']


def get_all_pages(posts):
    all_posts=[]
    all_posts=posts['data']
    while(1):
        try:
            nxt_page_url=posts['paging']['next']
        except KeyError:
            break
        posts=requests.get(nxt_page_url).json()
        all_posts+=posts['data']
    return all_posts


def get_user_details():
   user = graph.get_object('me',fields='name,id,email,education,friends')
   return user



def get_liked_page():
    pages=graph.get_connections('me',connection_name='likes')
    mypages=get_all_pages(pages)
    #print(pages)
    return mypages


def get_post_likes(post):
   mylikes=[]
   try:
     likes=graph.get_connections(post['id'],"likes")
     mylikes = get_all_pages(likes)
   except:
     pass
   return mylikes




def get_user_post(): # it will generate all d post of the user
    my_post=[ ]
    posts=graph.get_connections('me',connection_name='posts')
    mypost=get_all_pages(posts)
    return mypost




def time_line(): # this will create time line reviews and convert a word cloud of them
    myposts=graph.get_connections('me',connection_name='feed')
    all_posts=get_all_pages(myposts)
    print("post found on your timeline")
    all_text=''.join(post['message'] for post in all_posts if 'message' in post)
    wc=WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=200,
                          height=300).generate(all_text)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

time_line()


# like details of your post according to your frnds  ## abhi adhura h pura krna h
def get_like_details():
    myposts=get_user_post()
    print("post found on your wall")
    for post in myposts:
        mylikes=get_post_likes(post)

