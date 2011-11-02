# Create your views here.

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from world.models import *
import simplejson
from django.contrib.gis.geos import Point
from django.http import HttpResponse
def index(request):
    'Display Map'
    waypoints = Waypoint.objects.order_by('name')
    data = {'waypoints' : waypoints,
        'content' : render_to_string('world/waypoint.html',
        {'waypoints' : waypoints})}

    return render_to_response('world/index.html',data )

def save(request):
    'Save waypoints'
    print "geldi.."
    for waypointString in request.POST.get('waypointsPayload', '').splitlines():
        waypointID, waypointX, waypointY = waypointString.split()
        waypoint = Waypoint.objects.get(id=int(waypointID))
        waypoint.geometry.set_x(float(waypointX))
        waypoint.geometry.set_y(float(waypointY))
        waypoint.save()
    return HttpResponse(simplejson.dumps(dict(isOk=1)),  mimetype='application/json')

def search(request):
    'Search waypoints'
    # Build searchPoint
    print "geldi."
    try:
        searchPoint = Point(float(request.GET.get('lng')), float(request.GET.get('lat')))
    except:
        return HttpResponse(simplejson.dumps(dict(isOk=0, message='Could not parse search point')))
    # Search database
    waypoints = Waypoint.objects.distance(searchPoint).order_by('distance')
    # Return
    return HttpResponse(simplejson.dumps(dict(
        isOk=1,
        content=render_to_string('world/waypoint.html', {
            'waypoints': waypoints
        }),
        waypointByID=dict((x.id, {
            'name': x.name,
            'lat': x.geometry.y,
            'lng': x.geometry.x,
        }) for x in waypoints),
    )), mimetype='application/json')

