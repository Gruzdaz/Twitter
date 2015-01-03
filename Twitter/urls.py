from django.conf.urls import patterns, include, url
from django.contrib import admin

from Main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'registracija.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', register, name='register'),
    url(r'^$', home_page, name='home_page'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^notification/$', notification, name='notification'),
    url(r'^(?P<username>\w+)/$', timeline, name='timeline'),
    url(r'^favourited/(?P<tweetsid>\d+)/', favourited, name='favourited'),
    url(r'^retweeted/(?P<tweetsid>\d+)/', retweeted, name='retweeted'),
    url(r'^reply/(?P<tweetsid>\d+)/', reply, name='reply'),
    url(r'^following/(?P<usersid>\d+)/', following, name='following'),
    url(r'^followers/(?P<usersid>\d+)/', followers, name='followers'),
    
)
