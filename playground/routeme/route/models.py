#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.auth.models import User


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
     people = models.ManyToManyField(User)
     owner = models.ManyToManyField(User, related_name = "owner")
