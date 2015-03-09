from django.db import models

# Create your models here.

class MyModel(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    author = models.CharField(max_length=20)

class Event(models.Model):
    name = models.CharField(max_length=100)

class BlogEntry(models.Model):
    name = models.CharField(max_length=50)

