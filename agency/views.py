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
from django.http import JsonResponse
from customer.utils import *


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

def order_approve_process(request, id):
    result = Order.objects.get(pk=id)
    try:
        user = User.objects.get(id=result.user_id)
        result.is_approve = 1
        result.save()
        messages.success(request, 'Order approved successfully!')
    except User.DoesNotExist:
        messages.error(request, 'User not found for this order')
    except Exception as e:
        messages.error(request, f'Error processing order: {str(e)}')
    return redirect("/agency/allOrder")

def Approved_Order(request):
    result = Order.objects.filter(is_approve=True)
    context = {'result': result}
    return render(request, 'agency/OrderApproved.html', context)

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
	return render(request, 'agency/ChangePassword.html')
	


from django.shortcuts import render, redirect
from django.http import JsonResponse


def SelectRegion(request):
    """Displays the region selection page with active states."""
    states = State.objects.filter(is_active=True, is_deleted=False).order_by('state_name')
    return render(request, 'agency/selectRegion.html', {'states': states})

def get_cities_list(request):
    """Fetches cities based on the selected state and previously selected cities."""
    state_id = request.GET.get("state_id")
    agency_id = request.session.get('super_agency_id')

    if not state_id:
        return JsonResponse({"error": "State ID is required"}, status=400)

    cities = list(City.objects.filter(state_id=state_id).values("id", "city_name"))

    # Fetch selected cities for the agency in the selected state
    selected_cities = AgencyRegion.objects.filter(agency_id=agency_id, state_id=state_id).values_list("city_id", flat=True)

    return JsonResponse({"cities": cities, "selected_cities": list(selected_cities)})

def selected_region(request):
    """Handles saving selected state and cities for an agency."""
    if request.method == "POST":
        agency_id = request.session.get('super_agency_id')
        state_id = request.POST.get('state')
        city_ids = request.POST.getlist('cities[]')

        if not (agency_id and state_id and city_ids):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Remove old selections and insert new ones
        AgencyRegion.objects.filter(agency_id=agency_id, state_id=state_id).delete()
        AgencyRegion.objects.bulk_create([
            AgencyRegion(agency_id=agency_id, state_id=state_id, city_id=int(city))
            for city in city_ids
        ])

        return redirect("/agency/dashboard")
    return JsonResponse({"error": "Invalid request"}, status=400)

def allRegion(request):
	"""Displays all selected regions for an agency."""
	agency_id = request.session.get('super_agency_id')
	print(agency_id)

    # Fetch agency regions efficiently with related state and city data
	agency_regions = AgencyRegion.objects.filter(agency_id=agency_id).select_related('state').prefetch_related('city')
	regions = []
	for region in agency_regions:
		state_name = region.state.state_name
		city_name = region.city.city_name if region.city else "Unknown"
		
		regions.append({
            "id": region.id,
            "state_name": state_name,
            "city_name": city_name
        })
	return render(request, 'agency/allregion.html', {'regions': regions})
	
def NewClassfiedTextOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',	u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Classified Text Ad' AND o.agency_id = %s AND o.is_approve = 0 AND o.is_printed = 0
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/newClassifiedTextOrder.html",{'result':result})

def classfiedTextOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',	u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Classified Text Ad' AND o.agency_id = %s AND o.is_approve = 1 AND o.is_printed = 0
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/classifiedTextOrder.html",{'result':result})

def approveOrder(request, id):
	"""Approves an order by setting its 'is_approve' status to 1."""
	try:
		order = Order.objects.get(pk=id)
		agency=Agency.objects.get(pk=order.agency_id)
		user = User.objects.get(pk=order.user_id)
		order.is_approve = 1
		order.save()  # Save the changes to the database
		messages.success(request, 'Order Approved Successfully!')
		send_order_approval_email(user,order,agency)
		return redirect(request.META.get('HTTP_REFERER', '/agency/NewClassfiedTextOrder'))
	except Order.DoesNotExist:
        # Handle the case where the order does not exist
		return HttpResponse("Order not found.")
	

def rejectOrder(request, id):
	pass 

def printOrder(request, id):
	"""Approves an order by setting its 'is_printed' status to 1."""
	try:
		order = Order.objects.get(pk=id)
		agency = Agency.objects.get(pk=order.agency_id)
		user = User.objects.get(pk=order.user_id)
		order.is_printed = 1
		send_ad_printed_email(user,order,agency)
		order.save()  # Save the changes to the database
		messages.success(request, 'Order Status Changed to Printed Successfully!')
		return redirect(request.META.get('HTTP_REFERER', '/agency/NewClassfiedTextOrder')) # Redirect to the new classified order page after approval
	except Order.DoesNotExist:
		return HttpResponse("Order not found.")

def printedClassifiedTextOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Classified Text Ad' AND o.agency_id = %s AND o.is_approve = 1 AND o.is_printed = 1
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/printedClassifiedTextOrder.html",{'result':result})

def classifiedTextOrderViewmore(request,id):
	orderResult = Order.objects.get(pk=id)
	orderCategory = AdCategory.objects.get(pk=orderResult.category_id)
	userResult = User.objects.get(pk=orderResult.user_id)
	userProfile = Profile.objects.get(user_id = orderResult.user_id)
	context = {
		'orderResult' : orderResult,
		'orderCategory' : orderCategory,
		'userResult' : userResult,
		'userProfile' : userProfile,
	}

	return render(request,'agency/orders/classifiedTextOrderViewmore.html',context);

def NewClassifiedDisplayOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',	u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Classified Display Ad' AND o.agency_id = %s AND o.is_approve = 0 AND o.is_printed = 0
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/newClassifiedDisplayOrder.html",{'result':result})

def classifiedDisplayOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',	u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Classified Display Ad' AND o.agency_id = %s AND o.is_approve = 1 AND o.is_printed = 0
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/classifiedDisplayOrder.html",{'result':result})

def printedClassifiedDisplayOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Classified Display Ad' AND o.agency_id = %s AND o.is_approve = 1 AND o.is_printed = 1
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/printedClassifiedDisplayOrder.html",{'result':result})
def NewDisplayOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',	u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Display Ad' AND o.agency_id = %s AND o.is_approve = 0 AND o.is_printed = 0
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/newDisplayOrder.html",{'result':result})

def DisplayOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',	u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Display Ad' AND o.agency_id = %s AND o.is_approve = 1 AND o.is_printed = 0
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/DisplayOrder.html",{'result':result})

def printedDisplayOrder(request):
	agency_id = request.session.get('super_agency_id')
	query = """
        SELECT o.id as id ,o.date, o.order_date, o.subject, o.price, 
		CONCAT(u.first_name,' ',u.last_name) as fullname,
		up.profile_image
        FROM `order` AS o
        INNER JOIN adcategory AS c ON c.id = o.category_id 
		JOIN auth_user as u ON u.id = o.user_id
		JOIN profile as up ON up.user_id = u.id
        WHERE c.classifiedtype = 'Display Ad' AND o.agency_id = %s AND o.is_approve = 1 AND o.is_printed = 1
    """
	result = Order.objects.raw(query, [agency_id])
	return render(request,"agency/orders/printedDisplayOrder.html",{'result':result})

def allInquiry(request):
	agency_id = request.session.get('super_agency_id')
	query = """
		SELECT ai.id, ai.subject, ai.message, ai.user_id, u.username, CONCAT(u.first_name,' ',u.last_name) as fullname, up.profile_image,ai.created_at 
		FROM agency_inquiry AS ai JOIN auth_user as u ON u.id = ai.user_id 
		JOIN profile as up ON up.id = ai.user_id
		WHERE ai.agency_id = %s AND ai.is_active = 1 AND ai.is_deleted = 0
		ORDER BY ai.created_at DESC
	"""
	result = AgencyInquiry.objects.raw(query, [agency_id])
	return render(request, "agency/allInquiry.html", {'result': result})
