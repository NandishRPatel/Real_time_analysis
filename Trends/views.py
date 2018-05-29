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
    trends_list = api.trends_place(1)
    #print(trends_list)
    trends_list = trends_list[0]['trends']
    list=[]
    for i in trends_list:
        list.append(i['name'])
    template = loader.get_template('list_trends.html')
    return HttpResponse(template.render({'trends':list}, request))