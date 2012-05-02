from django.conf.urls.defaults import *
from contact_importer.views import *

urlpatterns = patterns('',
    url(r'^import/$', view=contact_importer, name="contact_importer"),
    url(r'^(?P<importing_profile>\w+)$', view=contact_importer_home, name="contact_list"),
)
