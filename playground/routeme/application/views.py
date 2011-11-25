# Create your views here.

from django.shortcuts import render_to_response

def error404(request):
    return render_to_response("application/404.html")
