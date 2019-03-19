from django.conf.urls import url
from django.conf.urls import include
from .views import home
from .views import account

urlpatterns = [
    url(r'^$', home.index),
    url(r'^news/$', home.news),
    url(r'^pick/$', home.pick),
    url(r'^photo/$', home.photo),
    url(r'^get_imgs.html$', home.get_imgs),
    url(r'^login.html$', account.login),
    url(r'^logout.html$', account.logout),
    url(r'^register.html$', account.register),
    url(r'^check_code.html', account.checkcode, name='checkcode'),
    url(r'^up/$', home.up),
    url(r'^comment/$', home.comment),

    url(r'^(?P<site>\w+)/$', home.home),
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*)/$', home.filter),
    url(r'^(?P<site>\w+)/(?P<article_id>\d+)/$', home.article),


]