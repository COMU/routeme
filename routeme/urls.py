from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('routeme',
    # Examples:
    url(r'^', include('route.urls')),
    url(r'^email/', include('userprofile.urls')),
    url(r'^foursq/', include('foursq.urls')),
    url(r'^twitter/', include('twitter_app.urls')),
    url(r'^facebook/', include('facebook.urls')),
    url(r'^message/', include('message.urls')),
    url(r'^friend/', include('friend.urls')),
    url(r'^contact/', include('contact_importer.urls')),
    # url(r'^$', 'routeme.views.home', name='home'),
    # url(r'^routeme/', include('routeme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


