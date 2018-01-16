from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
from .models import Example, RepositoryInfo


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
    result = requests.get('https://api.github.com/repos/%s/%s/commits' % ('igen-ftn', 'igenhub'))
    repo_info = RepositoryInfo('igen-ftn', 'igenhub', result.content)
    return render(request, 'igenapp/commits.html', {'repo_info': repo_info})

