from django.db import models

# Create your models here.

class Messages(models.Model):
	fb_id= models.CharField(max_length=128)
	name=models.CharField(max_length=50)
	profile_url= models.URLField(max_length=50)
	locale=models.CharField(max_length=50)
	gender=models.CharField(max_length=10)
	message=models.CharField(max_length=1000,default='hi')

	def __unicode__(self):
		return self.name