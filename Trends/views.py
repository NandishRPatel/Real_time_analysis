from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
import tweepy,json,re,os
from textblob import TextBlob
import matplotlib.pyplot as plt
from mtranslate import translate

ckey = "0HbmxMUQ5DczFuKbpUt1WFQA9"
csecret = "LjC1kTMY3LrnzBX8cMZrhTWLXXDRLBCa4ZSfXMwO42244V6O5U"
atoken = "2516974466-EyjU0m1wGFYJpYXoi88SGZQTtHk3PEtrkUdE4OK"
asecret = "VZGEEkH7HiytC3abwrTpTDmONsJ7SWbJkHD8XdjGSSzfF"

auth = tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

flag = []

data = {}

def trends(request):
    print(request.GET)
    trends_list = api.trends_place(1)
    trends_list = trends_list[0]['trends']
    list=[]
    for i in trends_list:
        temp = i['name']
        if (temp[0] == '#'):i['name'] = i['name'][1:]
        list.append(i['name'])
    template = loader.get_template('list_trends.html')
    return HttpResponse(template.render({'trends':list}, request))

class TweetStreamListener(tweepy.StreamListener):

    def __init__(self,api=None):
        super(TweetStreamListener,self).__init__()
        self.cnt = 1
        self.end = 50
        print("started")

    def on_status(self, status):
        d={}
        if self.end >= self.cnt:
            #print(json.dumps(status._json))
            #print(type(status._json['text']))
            d['text'] = status._json['text']
            d['user'] = status._json['user']['screen_name']
            d['id'] = status._json['user']['id_str']
            d['lang'] = status._json['user']['lang']
            d['sentiment'] = get_sentiment(d['text'])
            data[self.cnt] = d
            generate_graph()
            self.cnt+=1
        else:
            print('end')
            return False

    def on_error(self, status_code):
        print("error", status_code)
        return False

    def on_timeout(self):
        print('timeout')
        return False

def get_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

def clean_tweet(tweet): return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def generate_graph():
    sentiments = []
    names = []
    for i in data:
        sentiments.append(data[i]['sentiment'])
        names.append(i)
    pos = sentiments.count(1)
    neg = sentiments.count(-1)
    neu = sentiments.count(0)
    labels = ['Positive','Neutral','Negative']
    sizes = [pos,neg,neu]
    explode = (0.1, 0, 0)
    colors = ['gold', 'yellowgreen', 'lightcoral']
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=0)
    plt.axis('equal')
    plt.savefig(os.getcwd()+'/Trends/templates/trends/pie.png')
    plt.clf()


def hashtag_details(request):
    if not flag:
        streamListener = TweetStreamListener()
        myStream = tweepy.Stream(auth=api.auth,listener=streamListener)
        hashtag = ((request.path[1:]).split('='))[1]
        myStream.filter(track=hashtag,async=True)
        flag.append(1)
    else:pass

    template = loader.get_template('hashtag_details.html')
    return HttpResponse(template.render({'data': data}, request))