from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
from igenapp.models import Example


def index(request):
    return render(request, 'igenapp/index.html')

def insert(request, tea):
    #upis u bazu
    Example.objects.create(text=tea)
    #ispise sve upisane objekte
    return HttpResponse(Example.objects.all())

def home(request):
    return render(request, 'igenapp/home.html')

def wiki(request):
    return render(request, 'igenapp/wiki.html')

def issues(request):
    return render(request, 'igenapp/issues.html')

def commits(request):
    return render(request, 'igenapp/commits.html')

