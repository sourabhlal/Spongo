from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^$', 'spongoApp.views.miscellaneous.home'),
    url(r'^home/$', 'spongoApp.views.miscellaneous.home'),
    url(r'^settings/$', 'spongoApp.views.settings.home',name='home'),
    url(r'^testing/$', 'spongoApp.views.miscellaneous.testing',name='test'),
    url(r'^results/$', 'spongoApp.views.miscellaneous.results',name='results'),
)
