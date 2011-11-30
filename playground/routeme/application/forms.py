#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from models import GENDER_CHOICES

class UserForm(forms.Form):
    firstName = forms.CharField(max_length = 30)
    lastName = forms.CharField(max_length = 30)
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)
    birthdate = forms.DateField()
    gender = forms.ChoiceField(choices = GENDER_CHOICES)
