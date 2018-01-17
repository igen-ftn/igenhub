from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
import datetime

# Create your views here.
from .models import Example
from .models import *
from .forms import IssueForm


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
    #######################
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
    try:
        issue = Issue.objects.get(pk=issue_id)
        return render(request, 'igenapp/issues/new_issue.html', {'labels': label_list, 'milestones': milestone_list,
                                                                 'issue': issue})
    except Issue.DoesNotExist:
        return render(request, 'igenapp/issues/new_issue.html', {'labels': label_list, 'milestones': milestone_list})


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
                issue = Issue(title=form.cleaned_data['title'], text=form.cleaned_data['text'], ordinal=1, date=datetime.datetime.now())
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


def commits(request):
    return render(request, 'igenapp/commits.html')

