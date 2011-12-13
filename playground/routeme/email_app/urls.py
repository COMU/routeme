#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('routeme',
    # Examples:
    # url(r'^$', 'route.views.home', name='home'),
    # url(r'^route/', include('route.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^error$',"email.views.error404", name = "error"),
    url(r'^signup/$', "email.views.signup", name = "save-user"),
    url(r'^index/$', "email.views.index", name = "index"),
    url(r'login/$',"email.views.login",name = "login-user"),
    url(r'logout/$',"email.views.logout", name = "logout"),
)

