from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
import tweepy,json

ckey = "0HbmxMUQ5DczFuKbpUt1WFQA9"
csecret = "LjC1kTMY3LrnzBX8cMZrhTWLXXDRLBCa4ZSfXMwO42244V6O5U"
atoken = "2516974466-EyjU0m1wGFYJpYXoi88SGZQTtHk3PEtrkUdE4OK"
asecret = "VZGEEkH7HiytC3abwrTpTDmONsJ7SWbJkHD8XdjGSSzfF"

auth = tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

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
        self.end = 5
        print("started")

    def on_status(self, status):
        if self.end >= self.cnt:
            print(status._json['text'])
            print(type(status._json['text']))
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


def hashtag_details(request):
    streamListener = TweetStreamListener()
    myStream = tweepy.Stream(auth=api.auth,listener=streamListener)
    hashtag = ((request.path[1:]).split('='))[1]
    myStream.filter(track=hashtag,async=True)

    return HttpResponse("<h1>hashtag</h1>")