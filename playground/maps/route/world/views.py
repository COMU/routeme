# Create your views here.

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from world.models import *
from django.contrib.gis.geos import LineString, Point
from django.contrib.gis.measure import D
import simplejson
def index(request):
    return render_to_response("world/index.html")

def search(request):
    return render_to_response("world/search.html")

def save(request):
    pointList = []

    start = request.POST.get("start")
    end = request.POST.get("end")
    points = request.POST.get("waypoints")

    points = points.split("\n")

    for point in points :
        strPoint = point.split(",")
        pointList.append(Point(float(strPoint[0]), float(strPoint[1])))

    line = LineString(pointList)
    route = Route(start = start, end = end, coordinates = line)
    route.save()
    return HttpResponse("1")

def searchRoute(request):
    start = ""
    end = ""
    maxDistance = float(request.POST.get("distance"))
    try:
        start = Point(float(request.POST.get("lat1")),float( request.POST.get("lng1")))
        end = Point(float(request.POST.get("lat2")),float( request.POST.get("lng2")))
    except Exception:
        print Exception
    routes = Route.objects.filter(coordinates__distance_lt =(start, D(km=maxDistance))).filter(
            coordinates__distance_lt =(end, D(km=10)))
    print "before the dawn"
    content = render_to_string("world/routes.html",{ "routes": routes})
    print content
    return HttpResponse(simplejson.dumps(dict(isOk = 1,
        content = render_to_string("world/routes.html",{ "routes": routes}),
        )),mimetype='application/json')


