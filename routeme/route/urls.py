#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('routeme',
    url(r'^$',"route.views.index", name = "index"),
    url(r'^createroute$',"route.views.createRoute", name = "create-route"),
    url(r'^saverequest$',"route.views.saveRouteRequest", name = "save-request"),
    url(r'^searchroute$',"route.views.searchRoute", name = "search-route"),
    url(r'^listroute$',"route.views.listRoute", name = "list-route"),
    url(r'^returnroute/(?P<routeId>\d+)/',"route.views.returnRoute",name="return-route"),
)

