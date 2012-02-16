#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('message.views',
    url(r'^unread_count/$',"unread_count"),
)

