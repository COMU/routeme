#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.auth.models import User


ROUTE_APPROVAL = 0
ROUTE_WAITING = 1
ROUTE_REJECTED = 2

ROUTE_REQUEST_STATUS = {
	(ROUTE_APPROVAL,'appraval'),
	(ROUTE_WAITING,'waiting'),
	(ROUTE_REJECTED,'rejected'),
}


class RouteRequest(models.Model):
     person = models.ForeignKey(User)
     start = models.PointField()
     end = models.PointField()
     status = models.IntegerField(choices=ROUTE_REQUEST_STATUS)

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
     routerequest = models.ManyToManyField(RouteRequest,null=True)
     owner = models.ForeignKey(User, related_name = "owner")
     objects = models.GeoManager()

