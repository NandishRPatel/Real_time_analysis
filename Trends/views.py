from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader

def trends(request):
    return HttpResponse("<h1>YTreds</h1>")