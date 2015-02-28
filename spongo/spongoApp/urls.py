from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^', 'spongoApp.views.home'),
    url(r'^home/', 'spongoApp.views.home'),
    url(r'^settings/', 'spongoApp.views.settings'),
)
