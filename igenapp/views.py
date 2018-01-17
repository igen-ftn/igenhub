from django.shortcuts import render, redirect

from django.http import HttpResponse
from .forms import UserForm
# Create your views here.
from igenapp.models import Example
from igenapp.models import User


def index(request):
    return render(request, 'igenapp/index.html')

def insert(request, tea):
    #upis u bazu
    Example.objects.create(text=tea)
    #ispise sve upisane objekte
    return HttpResponse(User.objects.all())

def home(request):
    return render(request, 'igenapp/home.html')

def wiki(request):
    return render(request, 'igenapp/wiki.html')

def issues(request):
    return render(request, 'igenapp/issues.html')

def commits(request):
    return render(request, 'igenapp/commits.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('home')
    else:
        form = UserForm()
        return render(request, 'igenapp/signup.html', {'form':form})

def users(request, id):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.id = id
            user.save()
            return redirect('home')
        else:
            print("neuspeo update")
    else:
        user = User.objects.get(id=id)

        form = UserForm(initial = {'id': user.id, 'first_Name': user.first_Name, 'last_Name': user.last_Name, 'username': user.username, 'password': user.password, 'email': user.email})
        return render(request, 'igenapp/user_profile.html', {'form':form})


