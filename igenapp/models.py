from django.db import models

# Create your models here.


class Example(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Label(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    COLOR_CHOICE = (
        ('R', '#ee0701'),
        ('B', '#84b6eb'),
        ('Y', '#fbca04'),
        ('G', '#33aa3f'),
    )
    color = models.CharField(max_length=1, choices=COLOR_CHOICE)


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
    #comments
    #user
    #assignees
    label = models.ManyToManyField(Label)
    milestone = models.ForeignKey(Milestone, default=None, blank=True, null=True)



