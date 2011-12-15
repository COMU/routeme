#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('routeme',
    url(r'^$',"route.views.index", name = "index"),
    url(r'^createroute$',"route.views.createRoute", name = "create-route"),
    url(r'^saveroute$',"route.views.saveRoute", name = "save-route"),
)

