#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from models import GENDER_CHOICES
from django.forms.extras.widgets import SelectDateWidget


class UserForm(forms.Form):
    firstName = forms.CharField(max_length = 30)
    lastName = forms.CharField(max_length = 30)
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)
    birthdate = forms.DateField(widget = SelectDateWidget())
    gender = forms.ChoiceField(choices = GENDER_CHOICES)
    photo = forms.ImageField(required = False)
