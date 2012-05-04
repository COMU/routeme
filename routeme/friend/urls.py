#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('friend.views',
    url(r'^request/(?P<user_id>\d+)/$', "friendship_request", name="friendship_request"),
    url(r'^accept/(?P<request_id>\d+)$', "accept", name="friendship_accept"),
    url(r'^reject/(?P<request_id>\d+)$', "reject", name="friendship_reject"),
    url(r'^showStatus/(?P<user_id>\w+)$', "show_status", name="friendship_showstatus"),
    url(r'^list/$', "list", name="friendship_list"),
)

