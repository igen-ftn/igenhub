from django.db import models

# Create your models here.

class Example(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_Name = models.CharField(max_length=30, null = True)
    last_Name = models.CharField(max_length=30, null = True)
    username = models.CharField(max_length=40, default = "username")
    password = models.CharField(max_length=40, default = "password")
    email = models.CharField(max_length = 80, default="somebody@example.com")

    def __str__(self):
        return str(self.password) + self.username