from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^email/', include('routeme.email_app.urls')),
    url(r'^foursq_auth/', include('routeme.foursq.urls')),
    url(r'^twitter/', include('routeme.twitter_app.urls')),
    url(r'^facebook/', include('routeme.facebook.urls')),
    # url(r'^$', 'routeme.views.home', name='home'),
    # url(r'^routeme/', include('routeme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

