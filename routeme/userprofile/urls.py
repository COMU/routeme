#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('userprofile.views',
    # Examples:
    # url(r'^$', 'route.views.home', name='home'),
    # url(r'^route/', include('route.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^error$',"error404", name = "error"),
    url(r'^signup/$', "signup", name = "save-user"),
    url(r'login/$',"login",name = "login-user"),
    url(r'logout/$',"logout", name = "logout-user"),
    url(r'username/$',"get_username", name = "username"),
    url(r'update/$',"update",name = "update-user"),
    url(r'profile/(?P<userId>\d+)/$',"viewprofile", name = "view-profile"),
    url(r'activate/(?P<key>\w+)/$',"activate",name = "activate-user"),
)

