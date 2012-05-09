#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.auth.models import User


ROUTE_APPROVAL = 0
ROUTE_WAITING = 1
ROUTE_REJECTED = 2
ROUTE_CONFIRMED = 3

ROUTE_REQUEST_STATUS = (
	(ROUTE_APPROVAL,'appraval'),
	(ROUTE_WAITING,'waiting'),
	(ROUTE_REJECTED,'rejected'),
	(ROUTE_CONFIRMED,'confirmed'),
)

#Rota bilgileri
class RouteInformation(models.Model):
     date = models.DateField()
     time = models.TimeField()
     arrivalTime = models.CharField(max_length=10)
     vehicle = models.CharField(max_length=30)
     capacity = models.IntegerField()
     baggage = models.BooleanField()
     pet = models.BooleanField()
     route = models.LineStringField()
     owner = models.ForeignKey(User, related_name = "owner")
     start = models.CharField(max_length=50)
     end = models.CharField(max_length=50)
     private = models.BooleanField()
     objects = models.GeoManager()


class RouteRequest(models.Model):
     person = models.ForeignKey(User)
     start = models.PointField()
     end = models.PointField()
     startadress = models.CharField(max_length=200)
     stopadress = models.CharField(max_length=200)
     status = models.IntegerField(choices=ROUTE_REQUEST_STATUS)
     route = models.ForeignKey(RouteInformation)
