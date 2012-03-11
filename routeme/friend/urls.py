#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('friend.views',
    url(r'^request/(?P<user_id>\d+)$', "friendship_request", name="friendship_request"),
    url(r'^showStatus/(?P<user_id>\w+)$', "show_status", name="friendship_showstatus"),
)

