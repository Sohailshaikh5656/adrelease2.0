
from django.db import models
from django.contrib.auth.models import User
from datetime import *
from agency.models import *

class AdCategory(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	picture = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField(date.today)

class Agency(models.Model):
	username = models.CharField(max_length=255, unique = True)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length=255, default='default_password')
	isactive = models.BooleanField(default = True)
	approved = models.BooleanField(default = False)
	isBlocked = models.BooleanField(default=False)
	created_at = models.DateTimeField()
	updated_at = models.DateField(date.today)

	class Meta:
		db_table = 'Agency'
class Inquiry(models.Model):
	name = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	contact = models.BigIntegerField()
	message = models.TextField()
	date = models.DateField(default=date.today)

	class Meta:
		db_table = 'inquiry'
		
class Profile(models.Model):
	contact = models.BigIntegerField()
	gender = models.CharField(max_length=20)
	address = models.TextField()
	dob = models.DateField()
	reg_date = models.DateField(default=date.today)
	profile_image = models.CharField(max_length=255,null=True)
	user = models.OneToOneField(User,on_delete=models.CASCADE,default=None)

	class Meta:
		db_table = 'profile'

class User_feedback(models.Model):
	rating = models.CharField(max_length=30)
	message = models.TextField()
	date = models.DateField(default=date.today)
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)

	class Meta:
		db_table = 'feedback'
		
class Agencyprofile(models.Model):
	agencyname = models.CharField(max_length=100)
	ownername = models.CharField(max_length=50)
	contact = models.BigIntegerField()
	address =models.TextField()
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=100)
	est_date = models.DateField()
	reg_date = models.DateField(default=date.today)
	agency = models.OneToOneField(Agency,on_delete=models.CASCADE,default=None)
	class Meta:
		db_table = 'Agencyprofile'



class Addtocart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	ad = models.ForeignKey(Newadtype,on_delete=models.CASCADE,default=None)
	date = models.DateField(default=date.today)
	class Meta:
		db_table = 'add_to_cart'


class Order(models.Model):
	size = models.CharField(max_length=100)
	pageno = models.CharField(max_length=100)
	mode = models.CharField(max_length=50)
	order_date = models.DateField(default=date.today)
	date = models.DateField()
	subject = models.CharField(max_length=255)
	description = models.TextField()
	price = models.IntegerField()
	poster = models.CharField(max_length=255,null=True)
	word = models.CharField(max_length=255,null=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	agency = models.ForeignKey(Agency,on_delete=models.CASCADE,default=None)
	adType = models.ForeignKey(Newadtype, on_delete=models.CASCADE, null=False, blank=False)
	is_approve = models.BooleanField(default = 0)

	class Meta:
		db_table = 'order'

class Passwordall(models.Model):
	password_user = models.CharField(max_length=20)
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)

	class Meta:
		db_table = 'password'

class Payment(models.Model):
	amount = models.BigIntegerField()	
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	agency = models.ForeignKey(Agency,on_delete=models.CASCADE,default=None)
	adType = models.ForeignKey(Newadtype,on_delete=models.CASCADE,default=None)
	order_id = models.ForeignKey(Order,on_delete=models.CASCADE,default=None)
	date = models.DateField(default=date.today)

	class Meta:
		db_table='payment'

