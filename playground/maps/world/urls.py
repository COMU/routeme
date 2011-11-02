#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('maps.world.views',
        url(r'^$', 'index', name = 'world-index'),
        url(r'^save/$', 'save', name='world-save'),
        url(r'^search/$', 'search', name='world-search'),
)
