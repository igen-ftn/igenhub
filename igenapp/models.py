from django.db import models

# Create your models here.

class Example(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class RepositoryInfo:
    def __init__(self, owner_name, repo_name, commits):
        self.owner_name = owner_name
        self.repo_name = repo_name
        self.commits = commits
