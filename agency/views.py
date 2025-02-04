from django.shortcuts import render, redirect, HttpResponse
from agency.models import *
from customer.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.contrib import auth, messages
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views.generic import View
from .helpers import html_to_pdf 


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        query = request.user.id
        result = Order.objects.filter(agency_id=query)
        context = {'result':result}
        # getting the template
        pdf = html_to_pdf('pdf.html',context)
        return HttpResponse(pdf, content_type='application/pdf')


# Create your views here.
def dashboard(request):
	user_count = User.objects.count()
	order_count = Order.objects.count()
	agency_count = Agencyprofile.objects.count()
	return render (request,'agency/dashboard.html',{'user_count': user_count,'order_count':order_count,'agency_count':agency_count})


def register(request):
	context={}
	return render (request,'agency/register.html',context)


#inquiry

def agency_inquiry(request):
	context={}
	return render (request,'agency/inquiry.html',context)

def agency_inquiry_store(request):
	name = request.POST['name']
	contact = request.POST['contact']
	email = request.POST['email']
	message = request.POST['message']
	date = request.POST['date']

	Inquiry.objects.create(name=name, email=email, contact=contact, message=message, date=date)

	return redirect('/myadmin/inquiry_read')


def feedback(request):
	context={}
	return render (request,'agency/feedback.html',context)


def login(request):
	context={}
	return render (request,'agency/login.html',context)



def logout(request):
	auth.logout(request)
	return redirect('/customer/agency')

def payment(request):
	query = request.user.id
	print(query)
	result = Payment.objects.filter(agency_id=query)

	context={'result':result}
	return render(request,'agency/payment.html',context)



def add_agency(request):
	return render (request,'agency/register.html',context)



#-------------------------------------------------------------------

def Add_adtype(request):
	id = request.session['super_agency_id']
	page_numbers = range(1, 17)
	print(id)
	context={'page_numbers':page_numbers}
	return render(request,'agency/newad.html',context)

def Add_adtype_store(request):
	id = request.session['super_agency_id']
	title = request.POST['title']
	description = request.POST['description']
	size = request.POST['size']
	price = request.POST['price']
	pageno = request.POST['pageno']
	adtype = request.POST['adtype']

	myimage = request.FILES['image']
	mylocation = os.path.join(settings.MEDIA_ROOT, 'upload')
	obj = FileSystemStorage(location=mylocation)
	obj.save(myimage.name, myimage)

	Newadtype.objects.create(title=title,description=description,size=size,price=price,pageno=pageno,adtype=adtype,image=myimage.name,agency_id=id)
	return redirect('/agency/Add_adtype')


def  All_Adtype(request):
	# result = Newadtype.objects.all()
	query = request.session['super_agency_id']
	print(query)
	result = Newadtype.objects.filter(agency_id=query)

	context={'result':result}
	return render(request,'agency/all_adtype.html',context)


def All_Adtype_delete(request,id):
    result = Newadtype.objects.get(pk=id)
    result.delete()
    return redirect('/agency/All_Adtype')

def All_Adtype_edit(request,id):
	result = Newadtype.objects.get(pk=id)
	context = {'result':result}
	return render(request,'agency/add_edit.html',context)

def All_Adtype_update(request,id):
	myimage = request.FILES['image']
	mylocation = os.path.join(settings.MEDIA_ROOT, 'upload')
	obj = FileSystemStorage(location=mylocation)
	obj.save(myimage.name, myimage)
	data = {
	'title':request.POST['title'],
	'description':request.POST['description'],
	'size':request.POST['size'],
	'price':request.POST['price'],
	'pageno':request.POST['pageno'],
	'adtype':request.POST['adtype'],
	'image':myimage.name
	}
	Newadtype.objects.update_or_create(pk=id, defaults=data)
	return redirect('/agency/All_Adtype')

def order_front_page(request):
	agency_id = request.session['super_agency_id']
	result = Newadtype.objects.filter(agency_id=agency_id)
	context = {'result':result}
	return render(request,'agency/order_front_page.html',context)

def order(request):
	query = request.session['super_agency_id']
	adType_id = int(request.POST['adTypeData'])
	result = Order.objects.filter(agency_id=query,adType_id=adType_id, is_approve=False)
	context={'result':result}
	return render(request,'agency/order_read.html',context)

def allOrder(request):
	result = Order.objects.filter(is_approve=True)
	context={'result':result}
	return render(request,'agency/allOrder.html',context)

def order_approve_process(request,id):
	result = Order.objects.get(pk=id)
	result.is_approve = 1
	result.save()
	return redirect("/agency/allOrder")

def Approved_Order(request):
	result = Order.objects.filter(is_approve=True)
	context = {'result':result}
	return render(request,'agency/OrderApproved.html',context)

def order_viewmore(request,id):
    result = Order.objects.get(pk=id)
    context = {'result':result}
    return render(request,'agency/order_viewmore.html',context)


def profile(request,id):
	fkid = request.user.id
	result = User.objects.get(pk=id)
	result1 = Agencyprofile.objects.get(user_id = fkid)
	context = {'result1':result1}
	return render(request,'agency/profile.html',context)

def edit_profile(request,id):
	fkid = request.user.id
	result = User.objects.get(pk=id)
	result1 = Agencyprofile.objects.get(user_id = fkid)
	context = {'result1':result1}
	return render(request,'agency/edit_profile.html',context)

def agency_update(request,id):
	user = request.user.id
	result = Agencyprofile.objects.get(user_id=user)


	data = {
				'email': request.POST['email'],
				'username': request.POST['username']

			}

	data1 = {
				'contact': request.POST['contact'],
				'address': request.POST['address'],
				
				'agencyname': request.POST['agencyname'],
				'ownername': request.POST['ownername'],
				'address': request.POST['address'],
				'city': request.POST['city'],
				'state': request.POST['state'],
				
				'est_date': request.POST['est_date']


	}

	result = User.objects.update_or_create(pk=user, defaults=data)
	Agencyprofile.objects.update_or_create(user_id=user, defaults=data1)
	return redirect('/agency/dashboard')



def ChangePassword_chk(request):
	user_id = request.user.id
	username = request.POST['currentpass']
	passwd = request.POST['pass']
	cpasswd = request.POST['cpass']

	if passwd != cpasswd:
		messages.success(request, 'Confirm password does not match')
		return redirect('/agency/ChangePassword')
	if user_id is None:
		messages.success(request, 'Login First to Change Password')
		return redirect('/customer/agency')

	else :
		u= User.objects.get(username=username)
		u.set_password(passwd)
		u.save()
		data = {
				'password_user': passwd
				}
		Passwordall.objects.update_or_create(user_id=user_id, defaults=data)
		messages.success(request, 'Successfully Updated !! \nlogin first')
		return redirect('/customer/agency')
	


def ChangePassword(request):
	return render(request,'agency/ChangePassword.html')









