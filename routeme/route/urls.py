#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('routeme',
    url(r'^$',"route.views.index", name = "index"),
    url(r'^createroute$',"route.views.createRoute", name = "create-route"),
    url(r'^saverequest$',"route.views.saveRouteRequest", name = "save-request"),
    url(r'^searchroute$',"route.views.searchRoute", name = "search-route"),
    url(r'^offer$',"route.views.offerRoute", name = "offer-route"),
    url(r'^requestConfirm/(?P<requestId>\d+)/$',"route.views.requestConfirm", name = "confirm-request"),
    url(r'^requestReject/(?P<requestId>\d+)/$',"route.views.requestReject", name = "reject-request"),
    url(r'^listroute$',"route.views.listRoute", name = "list-route"),
    url(r'^returnroute/(?P<routeId>\d+)/',"route.views.returnRoute",name="return-route"),
    url(r'showroutedetail/(?P<routeId>\d+)/',"route.views.showRouteDetail",name="show-route-detail"),
    url(r'^leave/(?P<requestId>\d+)/',"route.views.leave",name="leave-route"),
    url(r'^confirm/(?P<requestId>\d+)/',"route.views.confirm",name="confirm-route"),
)

