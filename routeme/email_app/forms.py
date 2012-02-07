#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from models import GENDER_CHOICES
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core import validators

def userNameValidator(value):
    try:
        user = User.objects.get(username = value)
    except User.DoesNotExist:
        return True
    raise ValidationError('Email zaten var.')

class UserUpdateForm(forms.Form):
    firstName = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'title':"FirstName", 'placeholder': "First Name"}))
    lastName = forms.CharField(max_length = 30, widget = forms.TextInput(attrs = {'title':"LastName",'placeholder': "Last Name"}))
    email = forms.EmailField(widget = forms.TextInput(attrs={'placeholder':'Email'}),
				validators = [userNameValidator])
    photo = forms.ImageField(required = False)

class UserForm(forms.Form):
    firstName = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'title':"FirstName", 'placeholder': "First Name"}))
    lastName = forms.CharField(max_length = 30, widget=forms.TextInput(attrs={'placeholder': "Last Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Email"}),
            validators = [userNameValidator])
    password = forms.CharField(label = "Create Password", widget = forms.PasswordInput(attrs={'placeholder': "Password"}))
    password2 = forms.CharField(label = "Confirm Your Password", widget = forms.PasswordInput(attrs={'placeholder': "Password"}))
    birthdate = forms.DateField()
    gender = forms.ChoiceField(choices = GENDER_CHOICES)
    photo = forms.ImageField(required = False)

    def clean(self):
        super(forms.Form, self).clean()
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                self._errors['password'] = ["Parololar eşleşmeli."]
                self._errors['Password2'] = ["Parololar eşleşmeli."]
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

