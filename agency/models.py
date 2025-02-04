from django.db import models
from django.contrib.auth.models import User
from customer.models import *
from datetime import date

class Newadtype(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	size = models.CharField(max_length=100)
	price = models.BigIntegerField()
	pageno = models.CharField(max_length=30)
	adtype = models.CharField(max_length=30,default='')
	image = models.CharField(max_length=100)
	agency = models.ForeignKey('customer.Agency', on_delete=models.CASCADE, default=None)


	class Meta:
		db_table = 'New_AdType'

