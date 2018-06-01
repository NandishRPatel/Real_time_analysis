from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.trends,name='trends'),
    url(r'hashtag=\s*', views.hashtag_details,name='hashtag_details'),
]