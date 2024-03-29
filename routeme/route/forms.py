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
    messagecontent = forms.CharField(max_length=200,required=False)

class SearchRouteForm(forms.Form):
    where = forms.CharField(label="where")
    to = forms.CharField(label="to")
    start = forms.CharField(widget = forms.HiddenInput())
    end = forms.CharField(widget = forms.HiddenInput())
    date = forms.DateField(required=False)
    baggage = forms.BooleanField(required=False)
    pet = forms.BooleanField(required=False) 

class UpdateRouteForm(forms.Form):
    start = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    end = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    date = forms.DateField()
    time = forms.TimeField()
    arrivalTime = forms.CharField(max_length = 10)
    vehicle = forms.CharField(widget = Select(choices = [("Car","Car"), ("Truck", "Truck")]))
    capacity = forms.IntegerField(widget = Select(choices = [(x, str(x)) for x in range(1, 10)]))
    baggage = forms.BooleanField(required=False)
    pet = forms.BooleanField(required=False)

class CreateRouteForm(forms.Form):
    route = forms.CharField(widget = forms.HiddenInput())
    start = forms.CharField(widget = forms.HiddenInput())
    end = forms.CharField(widget = forms.HiddenInput())
    date = forms.DateField()
    time = forms.TimeField()
    arrivalTime = forms.CharField(max_length = 10)
    vehicle = forms.CharField(widget = Select(choices = [("Car","Car"), ("Truck", "Truck"), ("Motorsiklet", "Motorsiklet")]))
    capacity = forms.IntegerField(widget = Select(choices = [(x, str(x)) for x in range(1, 10)]))
    baggage = forms.BooleanField(required=False)
    pet = forms.BooleanField(required=False)
    private = forms.BooleanField(required=False)
