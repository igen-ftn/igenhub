from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Example(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class RepositoryInfo:
    def __init__(self, owner_name, repo_name, branches, commits, selected_branch='master'):
        self.owner_name = owner_name
        self.repo_name = repo_name
        self.branches = branches
        self.commits = commits
        self.selected_branch = selected_branch


class Repository(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, null=True)
    repo_name = models.CharField(max_length=70)
    owner_name = models.CharField(max_length=70)
    TYPE_CHOICE = (
        ('L', 'Local'),
        ('G', 'Git')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICE, default='L')
    url = models.CharField(max_length=150, default='')
    contributors = models.ManyToManyField(User, related_name='contributors')


class Label(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7)
    repository = models.ForeignKey(Repository, null=True)


class Milestone(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    creation_date = models.DateField()
    due_date = models.DateField(default=None, blank=True, null=True)
    STATUS_CHOICE = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='O')
    repository = models.ForeignKey(Repository, null=True)


class IssueHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True)
    text = models.CharField(max_length=50)
    date = models.DateTimeField()


class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    ordinal = models.IntegerField()
    date = models.DateTimeField()
    STATUS_CHOICE = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='O')
    history = models.ManyToManyField(IssueHistory)
    user = models.ForeignKey(User, null=True)
    assignee = models.ManyToManyField(User, related_name='issue_assignees')
    label = models.ManyToManyField(Label)
    milestone = models.ForeignKey(Milestone, default=None, blank=True, null=True)
    repository = models.ForeignKey(Repository, null=True)


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True)
    text = models.CharField(max_length=50)
    date = models.DateTimeField()
    link = models.CharField(max_length=100)
    repository = models.ForeignKey(Repository, null=True)


class WikiPage(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, null=True)
    issue = models.ForeignKey(to=Issue, null=True)
    wiki = models.ForeignKey(to=WikiPage, null=True)
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(null=True)

class UserImage(models.Model):
    user = models.OneToOneField(to=User, null=True, blank=True, primary_key=True, to_field='id')
    avatar = models.ImageField(upload_to='avatars', blank=True)