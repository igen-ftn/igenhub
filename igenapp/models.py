from django.db import models

# Create your models here.


class Example(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Issue(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    ordinal = models.IntegerField()
    date = models.DateField()
    status = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    #comments
    #user
    #assignees
    #label
    #milestone

    def __str__(self):
        return self.title + ' ' + self.text
