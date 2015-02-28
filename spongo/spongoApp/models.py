from django.db import models
from django.contrib.auth.models import User
import datetime

class userDetails(models.Model):
	GENDER = (
        ('F', 'Female'),
        ('M', 'Male')
    )
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	gender = models.CharField(max_length=1, choices=GENDER)
	currentTown =  models.CharField(max_length=25, blank = True, default="")
	email =  models.CharField(max_length=50)
	departures = models.CharField(max_length=15, blank = True, default="")
	def __unicode__(self):
		return self.name