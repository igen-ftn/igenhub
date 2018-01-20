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


def home(request):
    return render(request, 'igenapp/home.html')


def wiki(request):
    wikipages_list = WikiPage.objects.all()
    return render(request, 'igenapp/wiki.html', {'wikipages': wikipages_list})
    #return render(request, 'igenapp/wiki.html')


def wiki_form(request):
    if request.method == "POST":
        form = WikiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wiki')
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured:"
            return render(request, 'igenapp/wiki/form.html', context)
    else:
        form = WikiForm()
        return render(request, 'igenapp/wiki/form.html', {'form': form})


def issues(request):
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
                                                         text=form.cleaned_data['text'], ordinal=1, status='O')
                issue = get_object_or_404(Issue, pk=issue_id)
                if form.cleaned_data['milestone'] == 'null':
                    issue.milestone = None
                    issue.save()
            else:
                issue = Issue(title=form.cleaned_data['title'], text=form.cleaned_data['text'], ordinal=1,
                              date=datetime.datetime.now(), status='O', user=request.user)
                issue.save()
            if form.cleaned_data['milestone'] != 'null':
                milestone = get_object_or_404(Milestone, pk=form.cleaned_data['milestone'])
                issue.milestone = milestone
                issue.save()
            labels = request.POST.getlist('label')
            issue.label.clear()
            for label in labels:
                issue.label.add(label)
            assignees = request.POST.getlist('assignees')
            issue.assignee.clear()
            for assignee in assignees:
                issue.assignee.add(assignee)
            issue.save()
    else:
        form = IssueForm()

    issues_list = Issue.objects.order_by('-date')
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list})


def issue_details(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'igenapp/issues/issue_details.html', {'issue': issue})


def milestones(request):
    milestone_list = Milestone.objects.all()
    return render(request, 'igenapp/milestones/milestones.html', {'milestones': milestone_list})


def add_milestone(request):
    if request.method == "POST":
        form = MilestoneForm(request.POST)
        if form.is_valid():
            due_date = request.POST.get('due_date')
            if due_date == '':
                due_date = None
            Milestone.objects.create(title=form.cleaned_data['title'], description=form.cleaned_data['description'],
                                     creation_date=datetime.datetime.now(), due_date=due_date, status='O')
    else:
        form = MilestoneForm()

    milestone_list = Milestone.objects.all()
    return render(request, 'igenapp/milestones/milestones.html', {'milestones': milestone_list})


def remove_milestone(request, milestone_id):
    Milestone.objects.filter(pk=milestone_id).delete()
    milestone_list = Milestone.objects.all()
    return render(request, 'igenapp/milestones/milestones.html', {'milestones': milestone_list})


def labels(request):
    label_list = Label.objects.all()
    return render(request, 'igenapp/labels/labels.html', {'labels': label_list})


def add_label(request):
    if request.method == "POST":
        form = LabelForm(request.POST)
        if form.is_valid():
            Label.objects.create(name=form.cleaned_data['name'], color=form.cleaned_data['color'])
    else:
        form = LabelForm()

    label_list = Label.objects.all()
    return render(request, 'igenapp/labels/labels.html', {'labels': label_list})


def remove_label(request, label_id):
    Label.objects.filter(pk=label_id).delete()
    label_list = Label.objects.all()
    return render(request, 'igenapp/labels/labels.html', {'labels': label_list})


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
