#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.extras.widgets import SelectDateWidget, time, Select


class CreateRouteForm(forms.Form):
    route = forms.CharField(widget = forms.HiddenInput())
    date = forms.DateField(widget = SelectDateWidget())
    time = forms.TimeField()
    arrivalTime = forms.CharField(max_length = 10)
    vehicle = forms.CharField(max_length = 30)
    capacity = forms.IntegerField(widget = Select(choices = [(x, str(x)) for x in range(1, 10)]))
    baggage = forms.BooleanField()
    pet = forms.BooleanField()
