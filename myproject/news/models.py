from django.db import models

class Us(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    url_link = models.CharField(max_length=500)
    published_date = models.DateField()

class World(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    url_link = models.CharField(max_length=500)
    published_date = models.DateField()

class Politics(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    url_link = models.CharField(max_length=500)
    published_date = models.DateField()

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    url_link = models.CharField(max_length=500)
    published_date = models.DateField()
