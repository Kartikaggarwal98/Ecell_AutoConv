from django.db import models

# Create your models here.

class User(models.Model):
	fb_id= models.CharField(max_length=128)
	email=models.CharField(max_length=50)
	batch= models.URLField(max_length=50)

	def __unicode__(self):
		return self.email

class Messages(models.Model):
	fb_id= models.CharField(max_length=128)
	name=models.CharField(max_length=50)
	profile_url= models.URLField(max_length=50)
	locale=models.CharField(max_length=50)
	gender=models.CharField(max_length=10)
	message=models.CharField(max_length=1000,default='hi')

	#add date time stamp field
	def __unicode__(self):
		return self.name

