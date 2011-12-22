#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import CreateRouteForm, SearchRouteForm
from models import RouteInformation
from django.contrib.gis.geos import LineString, Point
from django.contrib.auth.models import User
from django.contrib.gis.measure import D

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/email/login")
    return render_to_response("route/index.html")

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

    data = { 'map': 1, "form": form}
    return render_to_response("route/createRoute.html", data)

def saveRoute(request):
    return -1
