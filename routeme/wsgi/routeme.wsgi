import os, sys
sys.path.append("/opt/routeme/")
sys.path.append("/opt/routeme/routeme")
os.environ['DJANGO_SETTINGS_MODULE'] = 'routeme.settings'

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
