#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from forms import CreateRouteForm, SearchRouteForm, StartEndPointForm
from models import RouteInformation,RouteRequest
from message.models import Message
from django.contrib.gis.geos import LineString, Point
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.template.loader import render_to_string
from django.db.models.manager import QuerySet

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/email/login")

    routeInfo = RouteInformation.objects.filter(owner = request.user)
    routeRequest = QuerySet(RouteRequest)
    for i in routeInfo:
	routeRequest = routeRequest | RouteRequest.objects.filter(route = i)
    unread_message_count = Message.objects.count_unread(request.user)
    return render_to_response("route/index.html",{'title':'Routeme','routeInfos':routeInfo, 'routeRequest':routeRequest,'unread':unread_message_count, "user":request.user})


def requestReject(request,requestId):
    if request.method == "POST":
	routeRequest = RouteRequest.objects.get(id=requestId)
	routeRequest.status = 2
	routeRequest.save()
	subject = "Route Request Confirm"
	content = "Your request is rejected by "+routeRequest.person.first_name
	Message.objects.create_message(request.user,routeRequest.person,subject,content) 
	return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def requestConfirm(request,requestId):
    if request.method == "POST":
	routeRequest = RouteRequest.objects.get(id=requestId)
	routeRequest.status = 0
	routeRequest.route.capacity =  routeRequest.route.capacity -1
	routeRequest.route.save()
	routeRequest.save()
	subject = "Route Request Confirm"
	content = "Your request is confirmed by "+routeRequest.person.first_name
	Message.objects.create_message(request.user,routeRequest.person,subject,content) 
	print routeRequest.status
	return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')
    


@login_required
def returnRoute(request,routeId):
    l = RouteInformation.objects.get(id=routeId).route.json
    print "returna geliyor"
    return render_to_response("route/listRoute.html",{'title':'Routeme','l':l,'map':1, 'unread':unread_message_count, "user":request.user})


@login_required
def saveRouteRequest(request):
    if request.method=="POST":
	form = StartEndPointForm(request.POST)
	if form.is_valid():
	    startpoint = form.cleaned_data['startpoint']
	    endpoint = form.cleaned_data['endpoint']
	    messagecontent = form.cleaned_data['messagecontent']
	    startaddress = form.cleaned_data['startaddress']
	    stopaddress = form.cleaned_data['stopaddress']
	    startpoint=startpoint.split(',')
	    endpoint=endpoint.split(',')
	    routeId = form.cleaned_data['routeowner']
	    route = RouteInformation.objects.get(id=routeId)
	    RouteRequest.objects.create(
		person = request.user,
		startadress = startaddress,
		stopadress = stopaddress,
		start = Point(float(startpoint[0]),float(startpoint[1])) ,
		end =  Point(float(endpoint[0]),float(endpoint[1])) ,
		route = route,
		status = 1,
	    )
	    subject = "Route Request"
	    content = messagecontent
	    Message.objects.create_message(request.user,route.owner,subject,messagecontent) 
	    return HttpResponseRedirect('/')
	return HttpResponseRedirect('/searchroute')
    return HttpResponseRedirect('/')
@login_required
def listRoute(request):
    if request.method=="POST":
        form = SearchRouteForm(request.POST)
        if form.is_valid():
            end = form.cleaned_data['end']
            start = form.cleaned_data['start']
            date = form.cleaned_data['date']
            baggage = form.cleaned_data['baggage']
            pet = form.cleaned_data['pet']
            end=end.split(',')
            start=start.split(',')
            end=Point(float(end[0]),float(end[1]))
            start=Point(float(start[0]),float(start[1]))
            print end
            print start
            route = RouteInformation.objects.filter(route__distance_lt = (start, D(km=10))).filter(route__distance_lt=(end,D(km=10))).filter(date=date).filter(pet=pet).filter(baggage=baggage).filter(capacity__gt=0)
	    # if route:
            unread_message_count = Message.objects.count_unread(request.user)
            form = StartEndPointForm()
            return render_to_response("route/listRoute.html",{'title':'Routeme','form':form,'routes':enumerate(route, 1),'map':1, 'unread':unread_message_count, "user":request.user})
    
    return HttpResponseRedirect('searchroute')


@login_required
def searchRoute(request):
    form = SearchRouteForm()
    unread_message_count = Message.objects.count_unread(request.user)
    data = { 'map': 1, "form": form, 'unread':unread_message_count, 'title':'Routeme',"user":request.user}
    return render_to_response("route/searchRoute.html", data)

@login_required
def createRoute(request):

    if request.method == "POST":
        form = CreateRouteForm(request.POST)
        if form.is_valid():
            #formdan gelen rota string seklinde.
            #gelen string parçalanıp LineString nesnesinde tutuluyor.
            points = form.cleaned_data['route'].split('\n')
            pointList = []
            for point in points:
                str = point.split(',')
                pointList.append(Point(float(str[0]), float(str[1])))

            lineString = LineString(pointList)
            routeInformation = RouteInformation.objects.create(
                        date = form.cleaned_data['date'],
                        time = form.cleaned_data['time'],
                        arrivalTime = form.cleaned_data['arrivalTime'],
                        vehicle = form.cleaned_data['vehicle'],
                        capacity = form.cleaned_data['capacity'],
                        baggage = form.cleaned_data['baggage'],
                        pet = form.cleaned_data['pet'],
                        route = lineString,
                        owner = request.user
                    )
            return HttpResponseRedirect("/")

    else:
        form = CreateRouteForm()
   
    unread_message_count = Message.objects.count_unread(request.user)
    data = { 'map': 1, "form": form, 'unread':unread_message_count, 'title':'Routeme',"user":request.user}
    return render_to_response("route/createRoute.html", data)

