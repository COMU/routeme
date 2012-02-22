#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.extras.widgets import SelectDateWidget, time, Select

class StartEndPointForm(forms.Form):
    startpoint = forms.CharField(widget = forms.HiddenInput())
    endpoint = forms.CharField(widget = forms.HiddenInput())
    routeowner = forms.CharField(widget = forms.HiddenInput())
    startaddress = forms.CharField(max_length=200,widget = forms.Textarea(attrs={'rows':4, 'cols':40}))
    stopaddress = forms.CharField(max_length=200,widget = forms.Textarea(attrs={'rows':4, 'cols':40}))

class SearchRouteForm(forms.Form):
    where = forms.CharField(label="where")
    to = forms.CharField(label="to")
    start = forms.CharField(widget = forms.HiddenInput())
    end = forms.CharField(widget = forms.HiddenInput())
    date = forms.DateField()
    baggage = forms.BooleanField(required=False)
    pet = forms.BooleanField(required=False) 

class CreateRouteForm(forms.Form):
    route = forms.CharField(widget = forms.HiddenInput())
    date = forms.DateField()
    time = forms.TimeField()
    arrivalTime = forms.CharField(max_length = 10)
    vehicle = forms.CharField(max_length = 30)
    capacity = forms.IntegerField(widget = Select(choices = [(x, str(x)) for x in range(1, 10)]))
    baggage = forms.BooleanField(required=False)
    pet = forms.BooleanField(required=False)
