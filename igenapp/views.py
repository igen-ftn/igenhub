from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

import datetime
import requests
import simplejson as json

from .models import *
from .forms import *

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
    #Issue.objects.all().delete()
    issues_list = Issue.objects.all()
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list})


def new_issue(request):
    milestone_list = Milestone.objects.all()
    label_list = Label.objects.all()
    return render(request, 'igenapp/issues/new_issue.html', {'labels': label_list, 'milestones': milestone_list})


def add_issue(request):
    print("OVDE")
    if request.method == "POST":
        form = IssueForm(request.POST)

        if form.is_valid():
            issue = Issue(title=form.cleaned_data['title'], text=form.cleaned_data['text'], ordinal=1,
                          date=datetime.datetime.now())
            issue.save()
            if form.cleaned_data['milestone'] != 'null':
                issue.milestone.add(form.cleaned_data['milestone'])
                issue.save()
            if form.cleaned_data['label'] != 'null':
                issue.label.add(form.cleaned_data['label'])
                issue.save()
    else:
        form = IssueForm()

    issues_list = Issue.objects.all()
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list})


def issue_details(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'igenapp/issues/issue_details.html', {'issue': issue})


def commits(request):
    result = requests.get('https://api.github.com/repos/%s/%s/commits' % ('igen-ftn', 'igenhub'))
    commits = json.loads(result.content)

    result = requests.get('https://api.github.com/repos/%s/%s/branches' % ('igen-ftn', 'igenhub'))
    branches = json.loads(result.content)

    repo_info = RepositoryInfo('igen-ftn', 'igenhub', branches, commits)

    return render(request, 'igenapp/commits/commits.html', {'repo_info': repo_info})


def commit(request, commit_id):
    result = requests.get('https://api.github.com/repos/%s/%s/commits/%s' % ('igen-ftn', 'igenhub', commit_id))
    commit = json.loads(result.content)
    commit['commit']['author']['date'] = commit['commit']['author']['date'].replace('T', ' ')[:-1]
    commit['allAdditions'] = sum([file['additions'] for file in commit['files']])
    commit['allDeletions'] = sum([file['deletions'] for file in commit['files']])

    return render(request, 'igenapp/commits/commit.html', {'commit': commit, 'owner_name': 'igen-ftn', 'repo_name': 'igenhub'})


def selected_branch(request):
    branch = request.GET.get('branch')
    result = requests.get('https://api.github.com/repos/%s/%s/commits?sha=%s' % ('igen-ftn', 'igenhub', branch))
    commits = json.loads(result.content)

    return JsonResponse(commits, safe=False)


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
            context['message'] = "Error has occured:"
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