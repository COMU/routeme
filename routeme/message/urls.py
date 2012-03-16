#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('message.views',
    url(r'^unread_count/$', "unread_count"),
    url(r'^inbox/$', "inbox", name="inbox"),
    url(r'^inbox/(?P<username>.+)/$', "inbox"),
    url(r'^markRead/$', "mark_read"),
)

