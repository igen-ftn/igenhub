from django.db import models

# Create your models here.

class Example(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class WikiPage(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
