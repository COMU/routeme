#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('routeme',
    url(r'^$',"route.views.index", name = "index"),
)

