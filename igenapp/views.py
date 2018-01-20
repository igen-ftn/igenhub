from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

import datetime
import requests
import simplejson as json

from .models import *
from .forms import *

from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    return render(request, 'igenapp/index.html')


def home(request, owner_name):
    return render(request, 'igenapp/home.html', {'owner_name': owner_name})


def wiki(request, owner_name, repo_name):
    wikipages_list = WikiPage.objects.all()
    return render(request, 'igenapp/wiki.html', {'wikipages': wikipages_list, 'owner_name': owner_name, 'repo_name': repo_name})
    #return render(request, 'igenapp/wiki.html')


def wiki_form(request, owner_name, repo_name):
    if request.method == "POST":
        form = WikiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wiki')
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured:"
            context['owner_name'] = owner_name
            context['repo_name'] = repo_name
            return render(request, 'igenapp/wiki/form.html', context)
    else:
        form = WikiForm()
        return render(request, 'igenapp/wiki/form.html', {'form': form, 'owner_name': owner_name, 'repo_name': repo_name})


def issues(request):
    #######################
    #User.objects.all().delete()
    #Issue.objects.all().delete()
    # Milestone.objects.all().delete()
    # Label.objects.all().delete()
    # Label.objects.create(name='bug', color='R')
    # Label.objects.create(name='feature', color='Y')
    # Milestone.objects.create(title='Milestone 1', description='This is first milestone', creation_date=datetime.datetime.now())
    ###########################
    issues_list = Issue.objects.order_by('-date')
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list})


def new_issue(request, issue_id):
    milestone_list = Milestone.objects.all()
    label_list = Label.objects.all()
    users = User.objects.all()
    try:
        issue = Issue.objects.get(pk=issue_id)
        return render(request, 'igenapp/issues/new_issue.html', {'labels': label_list, 'milestones': milestone_list,
                                                                 'issue': issue, 'users': users})
    except Issue.DoesNotExist:
        return render(request, 'igenapp/issues/new_issue.html', {'labels': label_list, 'milestones': milestone_list,
                                                                 'users': users})


def add_issue(request, issue_id):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            if int(issue_id) != 0:
                Issue.objects.filter(pk=issue_id).update(title=form.cleaned_data['title'],
                                      text=form.cleaned_data['text'], ordinal=1, date=datetime.datetime.now())
                issue = get_object_or_404(Issue, pk=issue_id)
                if form.cleaned_data['milestone'] == 'null':
                    issue.milestone = None
                    issue.save()
            else:
                issue = Issue(title=form.cleaned_data['title'], text=form.cleaned_data['text'], ordinal=1,
                              date=datetime.datetime.now())
                issue.save()
            if form.cleaned_data['milestone'] != 'null':
                milestone = get_object_or_404(Milestone, pk=form.cleaned_data['milestone'])
                issue.milestone = milestone
                issue.save()
            labels = request.POST.getlist('label')
            issue.label.clear()
            for label in labels:
                issue.label.add(label)
            issue.save()
    else:
        form = IssueForm()

    issues_list = Issue.objects.order_by('-date')
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list})


def issue_details(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'igenapp/issues/issue_details.html', {'issue': issue})


def commits(request, owner_name, repo_name):
    result = requests.get('https://api.github.com/repos/%s/%s/commits' % (owner_name, repo_name))
    commits = json.loads(result.content)

    result = requests.get('https://api.github.com/repos/%s/%s/branches' % (owner_name, repo_name))
    branches = json.loads(result.content)

    repo_info = RepositoryInfo(owner_name, repo_name, branches, commits)

    return render(request, 'igenapp/commits/commits.html', {'repo_info': repo_info})


def commit(request, owner_name, repo_name, commit_id):
    result = requests.get('https://api.github.com/repos/%s/%s/commits/%s' % (owner_name, repo_name, commit_id))
    commit = json.loads(result.content)
    commit['commit']['author']['date'] = commit['commit']['author']['date'].replace('T', ' ')[:-1]
    commit['allAdditions'] = sum([file['additions'] for file in commit['files']])
    commit['allDeletions'] = sum([file['deletions'] for file in commit['files']])

    return render(request, 'igenapp/commits/commit.html', {'commit': commit, 'owner_name': owner_name, 'repo_name': repo_name})


def selected_branch(request, owner_name, repo_name):
    branch = request.GET.get('branch')
    result = requests.get('https://api.github.com/repos/%s/%s/commits?sha=%s' % (owner_name, repo_name, branch))
    branch_info = {'owner_name': owner_name, 'repo_name': repo_name, 'commits': json.loads(result.content)}

    return JsonResponse(branch_info, safe=False)


def repositories(request, owner_name):
    return render(request, 'igenapp/repository/repository.html', {'owner_name': owner_name})


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
