from django import forms


class MessageForm(forms.Form):
 
    def __init__(self, kvargs):
	super(MessageForm, self).__init__()
        self.fields['to'].choices = kvargs

    to = forms.ChoiceField()
    subject = forms.CharField(widget=forms.TextInput(attrs={'title':"Subject", 'placeholder': "Subject"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'title':"Message", 'placeholder': "Message"}))
    

