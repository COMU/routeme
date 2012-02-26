from django import forms


class MessageForm(forms.Form):
    to = forms.CharField(widget=forms.TextInput(attrs={'title':"To", 'placeholder': "Username"}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'title':"Subject", 'placeholder': "Subject"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'title':"Message", 'placeholder': "Message"}))
    

