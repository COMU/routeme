from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('route.world.views',
    # Examples:
    # url(r'^$', 'route.views.home', name='home'),
    # url(r'^route/', include('route.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$',"index", name = "world-index"),
    url(r'^save/$',"save", name = "world-save"),
    url(r'^search/$',"search", name = "world-search"),
    url(r'^search-route/$',"searchRoute", name = "world-search-route"),
)
