from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
import datetime

# Create your views here.
from .models import Example
from .models import Issue
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
    issues_list = Issue.objects.all()
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list})


def new_issue(request):
    return render(request, 'igenapp/issues/new_issue.html')


def add_issue(request):
    if request.method == "POST":
        form = IssueForm(request.POST)

        if form.is_valid():
            Issue.objects.create(title=form.cleaned_data['title'], text=form.cleaned_data['text'], ordinal=1,
                                 date=datetime.datetime.now())
    else:
        form = IssueForm()

    issues_list = Issue.objects.all()
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list})


def issue_details(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    return render(request, 'igenapp/issues/issue_details.html', {'issue': issue})


def commits(request):
    return render(request, 'igenapp/commits.html')

