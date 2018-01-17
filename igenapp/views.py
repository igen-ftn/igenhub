from django.shortcuts import render, redirect, render_to_response

from django.http import HttpResponse
from .forms import UserForm, UserEditForm
# Create your views here.
from igenapp.models import Example
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    return render(request, 'igenapp/index.html')

def insert(request, tea):
    #upis u bazu
    Example.objects.create(text=tea)
    #ispise sve upisane objekte
    return HttpResponse(User.objects.get(id=1).password)

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
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured"
            return render(request, 'igenapp/signup.html', context)
    else:
        form = UserForm()
        return render(request, 'igenapp/signup.html', {'form':form})

def editUser(request):
    #nacin dobavljanja korisnika iz sesije je request.user
    user = request.user
    print("aaaa " + str(user.id))
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            context = dict()
            context['form'] = UserEditForm(instance = user)
            context['message'] = 'Your profile has been successfully updated!'
            return render(request, 'igenapp/user_profile.html', context)
        else:
            context = dict()
            context['form'] = form
            context['message'] = 'Error updating profile info. Please check input data!'
            return render(request, 'igenapp/user_profile.html', context)
    else:
        user = request.user
        context = dict()
        context['form'] = UserEditForm(instance=user)
        #form = UserEditForm(initial = {'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username, 'email': user.email})
        return render(request, 'igenapp/user_profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')