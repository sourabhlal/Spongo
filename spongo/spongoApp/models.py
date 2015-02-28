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

class CostOfLiving(models.Model):
	country_name = models.DecimalField(max_digits=8, decimal_places=2)
	accommodation = models.DecimalField(max_digits=8, decimal_places=2)
	food = models.DecimalField(max_digits=8, decimal_places=2)
	water = models.DecimalField(max_digits=8, decimal_places=2)
	local_transportation = models.DecimalField(max_digits=8, decimal_places=2)
	entertainment = models.DecimalField(max_digits=8, decimal_places=2)
	communication = models.DecimalField(max_digits=8, decimal_places=2)
	tips = models.DecimalField(max_digits=8, decimal_places=2)
	intercity_trasport = models.DecimalField(max_digits=8, decimal_places=2)
	souvenirs = models.DecimalField(max_digits=8, decimal_places=2)
	scams_robberies_mishaps = models.DecimalField(max_digits=8, decimal_places=2)
	alcohol = models.DecimalField(max_digits=8, decimal_places=2)