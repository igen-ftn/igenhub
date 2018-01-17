from django.db import models

# Create your models here.

class Example(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_Name = models.CharField(max_length=30)
    last_Name = models.CharField(max_length=30)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    email = models.CharField(max_length = 80)

    def __str__(self):
        return self.username