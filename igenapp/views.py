from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import datetime
import requests
import simplejson as json

from .models import *
from .forms import *


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

    return render(request, 'igenapp/commits/commit.html', {'commit': commit})


def selected_branch(request):
    branch = request.GET.get('branch')
    print(branch)
    result = requests.get('https://api.github.com/repos/%s/%s/commits/%s' % ('igen-ftn', 'igenhub', 'issues'))
    commits = json.loads(result.content)
    print(commits)
    return JsonResponse(commits)

