from django.db import models

class Us(models.Model):
	title = models.TextField()
	content = models.TextField()
	url_link = models.CharField(max_length=500)
	published_date = models.DateField()

class World(models.Model):
	title = models.TextField()
	content = models.TextField()
	url_link = models.CharField(max_length=500)
	published_date = models.DateField()

class Politics(models.Model):
	title = models.TextField()
	content = models.TextField()
	url_link = models.CharField(max_length=500)
	published_date = models.DateField()

class Business(models.Model):
	title = models.TextField()
	content = models.TextField()
	url_link = models.CharField(max_length=500)
	published_date = models.DateField()