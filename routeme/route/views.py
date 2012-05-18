#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from forms import CreateRouteForm, SearchRouteForm, StartEndPointForm,UpdateRouteForm
from models import RouteInformation,RouteRequest
from message.models import Message
from django.contrib.gis.geos import LineString, Point
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
from django.template.loader import render_to_string
from django.db.models.manager import QuerySet
from django.db.models import Q
from datetime import date as today
from friend.models import Friendship

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/email/login")

    routeInfo = RouteInformation.objects.filter(owner = request.user)
    myRequest = RouteRequest.objects.filter(person = request.user)    
    if routeInfo:
    	routeRequest = RouteRequest.objects.filter(route__in = routeInfo)    
    else:
        routeRequest = None
    return render_to_response("route/index.html",{'title':'Driverforme','routeInfos':routeInfo,'myRequests':myRequest, 'routeRequest':routeRequest, "user":request.user})



@login_required
def showRouteDetail(request, routeId):
    if request.method == "POST":
	form = UpdateRouteForm(request.POST)
	if form.is_valid():
	    routeInfo = RouteInformation.objects.get(id=routeId)
	    routeInfo.date = form.cleaned_data['date']
	    routeInfo.time = form.cleaned_data['time']
	    routeInfo.arrivalTime = form.cleaned_data['arrivalTime']
	    routeInfo.vehicle = form.cleaned_data['vehicle']
	    routeInfo.capacity = form.cleaned_data['capacity']
	    routeInfo.baggage = form.cleaned_data['baggage']
	    routeInfo.pet = form.cleaned_data['pet']
	    routeInfo.save()
	    return HttpResponseRedirect("/showroutedetail/"+str(routeInfo.id))
	return HttpResponseRedirect("/")
    else: 
    	routeInfo = RouteInformation.objects.get(id=routeId)
   	if routeInfo.owner == request.user:
    	    routeRequest = RouteRequest.objects.filter(route = routeInfo)
	    initial_data = {
		'start' :routeInfo.start,
		'end' :routeInfo.end,
		'date' : routeInfo.date,
		'time' : routeInfo.time,
		'arrivalTime' : routeInfo.arrivalTime,
		'vehicle' : routeInfo.vehicle,
		'capacity' : routeInfo.capacity,
		'baggage' : routeInfo.baggage,
		'pet' : routeInfo.pet
	   }
	    form = UpdateRouteForm(initial=initial_data)
    	    return render_to_response("route/routedetail.html",{'title':'driveforme','map':1,'form':form,'routeInfo':routeInfo,\
						'routeRequest':routeRequest,'user':request.user})
        else:
	    return HttpResponseRedirect('/')

@login_required
def leave(request, requestId):
    myRequest = RouteRequest.objects.get(id=requestId)
    route = myRequest.route
   
    myRequest.delete() #delete request and increase route capacity.
    route.capacity +=1
    route.save()

    #Send Message to route owner about that
    message = Message.objects.create_message(request.user, route.owner, "Route", "%s left from your route \
		which is on %s and from %s to %s." % \
		(request.user.get_full_name(), route.date, route.start, route.end))

    return HttpResponseRedirect(reverse('index'))    


@login_required
def confirm(request, requestId):
   myRequest = RouteRequest.objects.get(id=requestId)
   route = myRequest.route

   myRequest.status = 3 #Confirmed
   myRequest.save()
   
   #TODO this experience point must depends on requested person's distance between start and end points. 
   route.owner.userprofile.experience += 10 #increase user experience point.
   route.owner.userprofile.save()

   #Send Message to route owner about that 
   #TODO more user friendly message content will be good
   message = Message.objects.create_message(request.user, route.owner, "Route", "%s confirmed route \
                which is on %s and from %s to %s." % \
                (request.user.get_full_name(), route.date, route.start, route.end))

   return HttpResponseRedirect(reverse('index'))

@login_required
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

@login_required
def requestConfirm(request,requestId):
    if request.method == "POST":
	routeRequest = RouteRequest.objects.get(id=requestId)
	routeRequest.status = 0
	routeRequest.route.capacity =  routeRequest.route.capacity -1
	routeRequest.route.save()
	routeRequest.save()
	subject = "Route Request Confirm"
	content = "Your request is confirmed by "+request.user.first_name
	Message.objects.create_message(request.user,routeRequest.person,subject,content) 
	print routeRequest.status
	return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')
    


@login_required
def returnRoute(request,routeId):
    l = RouteInformation.objects.get(id=routeId).route.json
    print "returna geliyor"
    return render_to_response("route/listRoute.html",{'title':'Driveforme','l':l,'map':1, "user":request.user})


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
            route = RouteInformation.objects.filter(route__distance_lt = (start, D(km=10))).filter(route__distance_lt=(end,D(km=10)))
	    if date:
		route = route.filter(date=date)
	    else:
		route = route.filter(date__lte=today.today())
	    if pet == True and baggage == False:
		route = route.filter(pet=pet).filter(Q(baggage=baggage) | Q(baggage=not baggage)).filter(capacity__gt=0)
	    elif pet == False and baggage == True:
		route = route.filter(Q(pet=pet)|Q(pet= not pet)).filter(baggage=baggage).filter(capacity__gt=0)
	    elif pet == False and baggage == False:
		route = route.filter(Q(pet=pet)|Q(pet= not pet)).filter(Q(baggage=baggage) | Q(baggage=not baggage)).filter(capacity__gt=0)
	    else:
		route = route.filter(pet=pet).filter(baggage=baggage).filter(capacity__gt=0)

            route = list(route)
	    for r in route:
		if (r.private and not Friendship.objects.areFriends(request.user, r.owner)) or (r.owner == request.user):
			route.remove(r)			
	    # if route:
            form = StartEndPointForm()
            return render_to_response("route/listRoute.html",{'title':'Driveforme','form':form,'routes':enumerate(route, 1),'map':1, "user":request.user})
    
    return HttpResponseRedirect('searchroute')

@login_required
def offerRoute(request):
    lat = request.GET['lat']
    lng = request.GET['lng']
   
    point = Point(float(lat),float(lng))
    route = RouteInformation.objects.filter(route__distance_lt = (point, D(km=10)), date__gte=today.today())
    return render_to_response("route/listRoute.html",{'title':'Driveforme', 'routes':enumerate(route, 1),'map':1, "user":request.user})

@login_required
def searchRoute(request):
    form = SearchRouteForm()
    data = { 'map': 1, "form": form, 'title':'Driveforme',"user":request.user}
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
			start = form.cleaned_data['start'],
			end = form.cleaned_data['end'],
                        date = form.cleaned_data['date'],
                        time = form.cleaned_data['time'],
                        arrivalTime = form.cleaned_data['arrivalTime'],
                        vehicle = form.cleaned_data['vehicle'],
                        capacity = form.cleaned_data['capacity'],
                        baggage = form.cleaned_data['baggage'],
                        pet = form.cleaned_data['pet'],
 			private = form.cleaned_data['private'],
                        route = lineString,
                        owner = request.user
                    )
            return HttpResponseRedirect("/")

    else:
        form = CreateRouteForm()
   
    data = { 'map': 1, "form": form, 'title':'Driveforme',"user":request.user}
    return render_to_response("route/createRoute.html", data)

