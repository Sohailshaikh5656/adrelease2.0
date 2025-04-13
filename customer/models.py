from django.db import models
from django.contrib.auth.models import User
from datetime import *
from agency.models import *
from django.db.models import JSONField


class AdCategory(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	picture = models.CharField(max_length=255)
	classifiedtype = models.CharField(max_length=255,default='Classified Text Ad')
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'AdCategory'

class Agency(models.Model):
	username = models.CharField(max_length=255, unique = True)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length=255, default='default_password')
	isactive = models.BooleanField(default = True)
	approved = models.BooleanField(default = False)
	is_recomanded = models.BooleanField(default=False)
	isBlocked = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'Agency'

class Inquiry(models.Model):
	name = models.CharField(max_length=30)
	email = models.CharField(max_length=50)
	contact = models.BigIntegerField()
	message = models.TextField()
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	date = models.DateField(default=date.today)

	class Meta:
		db_table = 'inquiry'


class State(models.Model):
	id = models.AutoField(primary_key=True)
	state_name = models.CharField(max_length=100, unique=True)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'state'
    

class City(models.Model):
	id = models.AutoField(primary_key=True)
	city_name = models.CharField(max_length=100)
	state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'city'
		
class Agencyprofile(models.Model):
	agencyname = models.CharField(max_length=100)
	ownername = models.CharField(max_length=50)
	contact = models.BigIntegerField()
	address = models.TextField()
	city = models.ForeignKey(City, on_delete=models.SET_DEFAULT, default=1)
	state = models.ForeignKey(State, on_delete=models.SET_DEFAULT, default=1)
	est_date = models.DateField()
	reg_date = models.DateField(default=date.today)
	per_word_rate = models.BigIntegerField(default=0)
	circulation = models.BigIntegerField(default=0)
	profile_picture = models.TextField(default="image.jpg")
	cm_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	pan_number = models.CharField(max_length=20, default="")
	pan_photo = models.TextField(default="pan.jpg")
	gst_number = models.CharField(max_length=20, default="")
	adhare_number = models.BigIntegerField(default=0)
	adhare_photo = models.TextField(default="adhare.jpg")
	client_name = models.CharField(max_length=100, default="")
	agency = models.OneToOneField('Agency', on_delete=models.CASCADE, default=None)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'Agencyprofile'
		
class Profile(models.Model):
	contact = models.BigIntegerField()
	gender = models.CharField(max_length=20)
	address = models.TextField()
	dob = models.DateField()
	reg_date = models.DateField(default=date.today)
	profile_image = models.CharField(max_length=255,null=True)
	user = models.OneToOneField(User,on_delete=models.CASCADE,default=None)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'profile'

class User_feedback(models.Model):
	rating = models.IntegerField(default=1,null=True)
	message = models.TextField()
	date = models.DateField(default=date.today)
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'feedback'
		
class Order(models.Model):
	height = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	width = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	pageno = models.CharField(max_length=100,null=True)
	mode = models.CharField(max_length=50)
	order_date = models.DateField(default=date.today)
	date = models.DateField()
	subject = models.CharField(max_length=255)
	description = models.TextField(default=None, null=True)
	price = models.IntegerField()
	poster = models.CharField(max_length=255,null=True)
	word = models.CharField(max_length=255,null=True)
	category = models.ForeignKey(AdCategory,on_delete=models.CASCADE,default=None)
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	agency = models.ForeignKey(Agency,on_delete=models.CASCADE,default=None)
	any_preferance = models.TextField(default=None, null=True)
	ad_color = models.CharField(max_length=255, default=None)
	is_printed = models.BooleanField(default=0)
	is_approve = models.BooleanField(default = 0)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'order'


class Payment(models.Model):
	amount = models.BigIntegerField()	
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
	agency = models.ForeignKey(Agency,on_delete=models.CASCADE, default=None)
	adType = models.ForeignKey(Newadtype,on_delete=models.CASCADE, default=None)
	order_id = models.ForeignKey(Order,on_delete=models.CASCADE, default=None)
	date = models.DateField(default=date.today)
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'payment'


class AgencyRegion(models.Model):
	agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
	state = models.ForeignKey(State, on_delete=models.CASCADE)
	city = models.ForeignKey(City,on_delete=models.CASCADE)  
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'agencyregion'
	
class ForgetPassword(models.Model):
	email = models.CharField(max_length=255, null=True)
	username = models.CharField(max_length=150, null=True)
	token = models.CharField(max_length=255, unique=True)
	expiry_date_time = models.DateTimeField()
	is_active = models.BooleanField(default=True)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'forget_password'


class AgencyInquiry(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agency_inquiry'

