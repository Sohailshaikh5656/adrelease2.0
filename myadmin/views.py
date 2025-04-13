from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages

from customer.models import Order, Profile
from .approve import send_mail_to_user
from .reject import send_mail_of_reject
from django.core.mail import send_mail
import os
from django.core.exceptions import ObjectDoesNotExist
from .helper1 import send_forget_password_mail
from django.http import HttpResponse
from django.views.generic import View
from .helpers import html_to_pdf 
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import *

from PIL import Image
from rembg import remove
from customer.utils import *


class UserGeneratePDF(View):
    def get(self, request, param, *args, **kwargs):
        param = param.lower()
        context = {}
        if param == "newuser":
            query = """SELECT u.id, u.username, u.first_name, u.last_name, u.email, p.contact, p.gender, p.address, p.dob, p.profile_image 
                      FROM auth_user AS u 
                      JOIN profile AS p ON p.user_id = u.id 
                      WHERE DATE_ADD(u.date_joined, INTERVAL 1 DAY) > CURRENT_TIMESTAMP"""
            result = User.objects.raw(query)
            context = {'result': result, 'type': param, 'reportType': 'New / Recent Users Report'}
        
        elif param == "activeinactive":
            query = """SELECT u.id, u.username, u.first_name, u.last_name, u.email, p.contact, p.gender, p.address, p.dob, p.profile_image 
                      FROM auth_user AS u 
                      JOIN profile AS p ON p.user_id = u.id 
                      WHERE u.last_login > DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 MONTH)"""
            query2 = """SELECT u.id, u.username, u.first_name, u.last_name, u.email, p.contact, p.gender, p.address, p.dob, p.profile_image 
                       FROM auth_user AS u 
                       JOIN profile AS p ON p.user_id = u.id 
                       WHERE u.last_login < DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 MONTH)"""
            result = User.objects.raw(query)
            result2 = User.objects.raw(query2)
            context = {
                'result': result,
                'result2': result2,
                'type': param,
                'reportType': 'Active Users Report',
                'reportType2': 'Inactive Users Report'
            }
        
        elif param == "topbuyer":
            query = """SELECT u.id, COUNT(*) as count, p.profile_image, u.username, 
                      CONCAT(u.first_name,' ',u.last_name) as fullname 
                      FROM `order` AS o 
                      JOIN auth_user AS u ON o.user_id = u.id 
                      JOIN profile AS p ON p.user_id = u.id 
                      GROUP BY u.id"""
            result = Order.objects.raw(query)
            context = {'result': result, 'type': param, 'reportType': "Topbuyer"}
        
        elif param == "blockuser":
            query = """SELECT u.id, p.profile_image, u.username, 
                      CONCAT(u.first_name," ",u.last_name) as fullname 
                      FROM auth_user AS u 
                      JOIN profile AS p ON p.user_id = u.id 
                      WHERE u.is_active = 0"""
            result = Profile.objects.raw(query)
            context = {'result': result, 'type': param, 'reportType': "Blocked User"}

        else:
            return HttpResponse("Invalid report type", status=400)

        try:
            pdf = html_to_pdf('myadmin/report/user/reportPDF.html', context)
            if pdf:
                return HttpResponse(pdf, content_type='application/pdf')
            else:
                return HttpResponse("Failed to generate PDF", status=500)
        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

def agencyReportPDF(request, param):
    param = param.lower()

    if param == "newagency":
        query = """
        SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
               p.est_date, p.profile_picture 
        FROM agency AS a 
        JOIN agencyprofile AS p ON p.agency_id = a.id 
        JOIN state AS s ON s.id = p.state_id 
        JOIN city AS c ON c.id = p.city_id 
        WHERE DATE_ADD(a.created_at, INTERVAL 1 DAY) > CURRENT_TIMESTAMP
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'New / Recent Agency Report'
        }

    elif param == "activeinactive":
        query_active = """
            SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
                p.est_date, p.profile_picture
            FROM agency AS a 
            JOIN agencyprofile AS p ON p.agency_id = a.id  
            WHERE DATE(a.updated_at) >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        """

        query_inactive = """
            SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
                p.est_date, p.profile_picture 
            FROM agency AS a 
            JOIN agencyprofile AS p ON p.agency_id = a.id 
            WHERE DATE(a.updated_at) <= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        """

        result = Agency.objects.raw(query_active)
        result2 = Agency.objects.raw(query_inactive)

        context = {
            'result': result,
            'result2': result2,
            'type': param,
            'reportType': 'Active Agency Report',
            'reportType2': 'Inactive Agency Report'
        }

    elif param == "notapprove":
        query = """
        SELECT a.id, p.profile_picture, a.username, p.agencyname 
        FROM agency AS a 
        JOIN agencyprofile AS p ON p.agency_id = a.id 
        WHERE a.isBlocked = 0 AND a.approved = 0
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': "Not Approved Agencies"
        }

    elif param == "blockagency":
        query = """
        SELECT a.id, p.profile_picture, a.username, p.agencyname 
        FROM agency AS a 
        JOIN agencyprofile AS p ON p.agency_id = a.id 
        WHERE a.is_blocked = 1
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': "Blocked Agency"
        }
    else:
        return HttpResponse("Invalid report type", status=400)

    try:
        pdf = html_to_pdf('myadmin/report/agency/reportPDF.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return HttpResponse("Failed to generate PDF", status=500)
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

def trendingReportPDF(request, param):
    param = param.lower()
    
    if param == "trendingagency":
        query = """
        SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
               p.est_date, p.profile_picture, COUNT(o.id) as order_count
        FROM agency AS a
        JOIN agencyprofile AS p ON p.agency_id = a.id
        LEFT JOIN `order` AS o ON o.agency_id = a.id
        WHERE DATE(o.created_at) >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        GROUP BY a.id
        ORDER BY order_count DESC
        LIMIT 10
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Top Trending Agencies'
        }

    elif param == "trendingcategory":
        query = """
        SELECT c.id, c.name, c.classifiedtype, COUNT(o.id) as order_count,
               RANK() OVER (ORDER BY COUNT(o.id) DESC) as rank
        FROM adcategory AS c
        LEFT JOIN `order` AS o ON o.category_id = c.id
        WHERE DATE(o.created_at) >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        GROUP BY c.id
        ORDER BY order_count DESC
        LIMIT 10
        """
        result = AdCategory.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Top Trending Categories'
        }
    else:
        return HttpResponse("Invalid report type", status=400)

    try:
        pdf = html_to_pdf('myadmin/report/trending/reportPDF.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return HttpResponse("Failed to generate PDF", status=500)
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

def feedbackAndInquiryReportPDF(request, param):
    param = param.lower()
    
    if param == "feedback":
        query = """
        SELECT f.id, up.profile_image, u.username, f.rating, f.message, f.created_at
        FROM feedback AS f 
        JOIN auth_user AS u ON u.id = f.user_id 
        JOIN profile AS up ON up.user_id = f.user_id
        ORDER BY f.created_at DESC
        """
        result = User_feedback.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Customer Feedback Report'
        }
    
    elif param == "inquiry":
        query = """
        SELECT i.id, i.name, i.email, i.contact, i.message, i.created_at
        FROM inquiry AS i
        ORDER BY i.created_at DESC
        """
        result = Inquiry.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Customer Inquiry Report'
        }
    
    elif param == "agencyinquiry":
        query = """
        SELECT i.id, i.agency_id, a.username as agency, u.username as user, i.subject, i.message, i.created_at
        FROM agency_inquiry AS i 
        JOIN agency AS a ON a.id = i.agency_id
        JOIN auth_user AS u ON u.id = i.user_id
        ORDER BY i.created_at DESC
        """
        result = Inquiry.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Customer Inquiry Report'
        }
    
    else:
        return HttpResponse("Invalid report type", status=400)

    try:
        pdf = html_to_pdf('myadmin/report/feedbackAndInquiry/reportPDF.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return HttpResponse("Failed to generate PDF", status=500)
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

def pdf_gen(request):
    result = Newadtype.objects.all()
    context = {'result':result}
    return render(request,'pdf.html',context)




from customer.models import *

def dashboard(request):
    user_count = User.objects.count()
    order_count = Order.objects.count()
    agency_count = Agencyprofile.objects.count()
    id = request.user.id
    if id == None:
        return redirect('/myadmin/')
    else:
        return render(request,'myadmin/dashboard.html', {'user_count': user_count,'order_count':order_count,'agency_count':agency_count})

    # Pass the visitor count to the template
    
    

# Create your views here.
def login(request):
    context={}
    return render(request,'myadmin/login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('/myadmin/')



def admin_login_check(request):
    try:
         username = request.POST['username']
         password = request.POST['password']
         result1 = User.objects.get(username=username)
         result = auth.authenticate(request, username=username,password=password)
         if result1.is_staff == 0:
            messages.success(request, 'Invalid Username or You are not Admin')
            print('Invalid Username or You are not Admin')
            return redirect('/myadmin/')
         if result is None:
            messages.success(request, 'Invalid Username or You are not Admin')
            print('Invalid Username or You are not Admin')
            return redirect('/myadmin/')
         else:
            auth.login(request, result)
            request.session["admin_id"] = result1.id
            return redirect('/myadmin/dashboard')

    except ObjectDoesNotExist:
         my_object = None
         messages.success(request, 'Invalid Username or You are not Admin')
         print('Invalid Username or You are not Admin')
         return redirect('/myadmin/')

    else:
        pass
   
   
#-----------------------------------------------------------
def agency(request):
    query = """
        SELECT ap.*, a.email, a.username from agency as a JOIN agencyprofile as ap ON ap.agency_id = a.id WHERE
        approved = 1 AND isBlocked = 0 AND isactive = 1  
    """
    result = Agency.objects.raw(query)
    context={'result':result}
    return render(request,'myadmin/agency.html',context)
def agency_viewmore(request,id):
    result = Agency.objects.get(pk=id)
    profile = Agencyprofile.objects.get(agency_id = result.id)
    context = {'result':result,'profile':profile}
    return render(request,'myadmin/agency_viewmore.html',context)


#-----------------------------------------------------------
def inquiry(request):
    context={}
    return render(request,'myadmin/inquiry.html',context)
def feedback(request):
    result = User_feedback.objects.all()
    context={'result':result}
    return render(request,'myadmin/feedback.html',context)
#------------------------------------------------------------

def customer(request):
   
    result = Profile.objects.all()
    context = {'result':result,}
    return render(request,'myadmin/customer.html',context)

def customer_viewmore(request,id):
    result  = Profile.objects.get(pk=id)
    context = {'result':result}
    return render(request,'myadmin/customer_viewmore.html',context)

#-----------------------------------------------------------------

def order(request):
    result = Order.objects.all()
    context={'result':result}
    return render(request,'myadmin/order_read.html',context)

def order_viewmore(request,id):
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


#------------------------------------------------------------------
#customer


def inquiry_read(request):
    result = Inquiry.objects.all()
    context = {'result':result}
    return render(request,'myadmin/inquiry_read.html',context)

def inquiry_delete(request,id):
    result = Inquiry.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/inquiry_read')

def feedback_delete(request,id):
    result = User_feedback.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/feedback')

def admin_order(request):
    result = Order.objects.all()
    context = {'result':result}
    return render(request,'myadmin/approve_order.html',context)

def approve(request,id):
    result = Order.objects.get(pk=id)
    user = result.user_id
    result1 = User.objects.get(pk=user)
    email = result1.email
    fname = result1.first_name
    lname = result1.last_name
    send_mail_to_user(email)

    result.delete()
    messages.success(request, 'Order has been Approved and Order to Sent to Agency')
    return redirect('/myadmin/admin_order')

def approve(request,id):
    result = Order.objects.get(pk=id)
    user = result.user_id
    result1 = User.objects.get(pk=user)
    email = result1.email
    fname = result1.first_name
    lname = result1.last_name
    send_mail_to_user(email,fname,lname)

    size = result.size
    pageno = result.pageno
    mode = result.mode
    subject = result.subject
    description = result.description
    price = result.price
    user = result.user_id
    agency = result.agency_id
    poster = result.poster
    date = result.date
    order_date = result.order_date
    word = result.word
    Order_approve.objects.create(size=size,pageno=pageno,mode=mode,date=date,subject=subject,description=description,price=price,user_id=user,agency_id=agency,order_date=order_date,poster=poster,word=word)


    result.delete()
    messages.success(request, 'Order has been Approved and Order Sent to Agency')
    return redirect('/myadmin/admin_order')

def reject(request,id):
    result = Order.objects.get(pk=id)
    user = result.user_id
    result1 = User.objects.get(pk=user)
    email = result1.email
    fname = result1.first_name
    lname = result1.last_name
    send_mail_of_reject(email,fname,lname)

    result.delete()
    messages.success(request, 'Order has been Rejected')
    return redirect('/myadmin/admin_order')
def ChangePassword_chk(request):
    user_id = request.user.id
    username = request.POST['currentpass']
    passwd = request.POST['pass']
    cpasswd = request.POST['cpass']

    if passwd != cpasswd:
        messages.success(request, 'Confirm password does not match')
        return redirect('/myadmin/ChangePassword')
    if user_id is None:
        messages.success(request, 'Login First to Change Password')
        return redirect('/myadmin/')

    else :
        u= User.objects.get(username=username)
        u.set_password(passwd)
        u.save()
        data = {
                'password_user': passwd
                }
        Passwordall.objects.update_or_create(user_id=user_id, defaults=data)
        messages.success(request, 'Successfully Updated !! \nlogin first')
        return redirect('/myadmin/')


def ChangePassword(request):
    return render(request,'myadmin/ChangePassword.html')


def ForgetPassword(request):

    
    return render(request,'myadmin/forgetpassword.html')


def ForgetPassword_chk(request):

    username = request.POST['username']
    result = User.objects.get(username=username)
    user_id = result.id
    result1 = Passwordall.objects.get(user_id = user_id)

    if result is None:
        messages.success(request, 'Invalid Username ')
        print('Invalid Username')
        return redirect('/myadmin/ForgetPassword')
    elif result.is_staff == 0:
        messages.success(request, 'Invalid Username ')
        print('Invalid Username')
        return redirect('/myadmin/ForgetPassword')

    else:
        email = result.email
        
        username = result.username
        password = result1.password_user
        
        send_forget_password_mail(email,password,username)
        messages.success(request, 'Check Your Mail ')
    
    
    return redirect('/myadmin/ForgetPassword')
    

def agency_Approve(request):
    query = """
        SELECT a.id as id, ap.agencyname, a.email, a.username, c.city_name, st.state_name
    FROM agency as a
    JOIN agencyprofile as ap ON ap.agency_id = a.id 
    JOIN city as c ON c.id = ap.city_id
    JOIN state as st ON st.id = c.state_id 
    WHERE a.approved = 0 AND a.isBlocked = 0 AND a.isactive = 1
    """
    result = Agency.objects.raw(query)
    context = {'result':result}
    return render(request,'myadmin/agency_approve.html',context)

def agency_approve_process(request,id):
    result = Agency.objects.get(pk=id)
    result.approved = 1
    result.save()
    return redirect('/myadmin/agency_Approve')


def blocked_Agency(request):
    query = """
    SELECT a.id as id, ap.agencyname, a.email, a.username, c.city_name, st.state_name
    FROM agency as a
    JOIN agencyprofile as ap ON ap.agency_id = a.id 
    JOIN city as c ON c.id = ap.city_id
    JOIN state as st ON st.id = c.state_id 
    WHERE a.approved = 1 AND a.isBlocked = 1 AND a.isactive = 1
"""


    result = Agency.objects.raw(query)
    context = {'result':result}
    return render(request,'myadmin/showAllBlockAgency.html',context)

def agency_block_process(request,id):
    result = Agency.objects.get(pk=id)
    result.isBlocked = 1
    send_agency_block_email(result)
    result.save()
    return redirect('/myadmin/blocked_Agency')

def unblocked_Agency(request):
    query = """
        SELECT a.id as id, ap.agencyname, a.email, a.username, c.city_name, st.state_name
    FROM agency as a
    JOIN agencyprofile as ap ON ap.agency_id = a.id 
    JOIN city as c ON c.id = ap.city_id
    JOIN state as st ON st.id = c.state_id 
    WHERE a.approved = 1 AND a.isBlocked = 1 AND a.isactive = 1 
    """
    result = Agency.objects.raw(query)
    context = {'result':result}
    return render(request,'myadmin/agency_Unblock.html',context)

def agency_unblock_process(request,id):
    result = Agency.objects.get(pk=id)
    result.isBlocked = 0
    send_agency_unblock_email(result)
    result.save()
    return redirect('/myadmin/unblocked_Agency')
# def feedback_read(request):
#     User_feedback = 
#     context={}
#     return render(request,'customer/feedback.html',context)

########################################################################################################


def customer_block_process(request,id):
    result = User.objects.get(pk=id)
    result.is_active = 0
    send_user_block_email(result)
    result.save()
    return redirect('/myadmin/customer')

def blocked_customer(request):
    result = Profile.objects.all()
    context = {'result':result}
    return render(request,'myadmin/customer_blocked.html',context)

def unblocked_customer(request):
    result = Profile.objects.all()
    context = {'result':result}
    return render(request,'myadmin/customer_unblock.html',context)

def customer_unblock_process(request,id):
    result = User.objects.get(pk=id)
    result.is_active = 1
    send_user_unblock_email(result)
    result.save()
    return redirect('/myadmin/customer')

def adcategory_page(request):
    context={}
    return render(request,'myadmin/addCategory.html',context)


import os
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image
from rembg import remove  # Import background remover

def adcategory_store(request):
    category_name = request.POST['category_name']
    description = request.POST['description']
    is_active = int(request.POST.get('active', 0)) == 1
    classifiedType = request.POST['classifiedtype']
    classifiedType = classifiedType.strip()

    # Handle image upload
    myimage = request.FILES.get('image')
    if myimage:
        mylocation = os.path.join(settings.MEDIA_ROOT, 'category')
        obj = FileSystemStorage(location=mylocation)
        
        # Define the image path
        original_image_path = os.path.join(mylocation, myimage.name)
        
        # Save the original uploaded image
        obj.save(myimage.name, myimage)
        
        # Process the image to remove background
        processed_image_path = os.path.join(mylocation, f"no_bg_{myimage.name}")

        with open(original_image_path, "rb") as input_file:
            image_data = input_file.read()
            output_data = remove(image_data)  # Remove background

        with open(processed_image_path, "wb") as output_file:
            output_file.write(output_data)

        # Use the processed image for storing in DB
        image_name = f"no_bg_{myimage.name}"
    else:
        image_name = None

    # Save category data with processed image
    AdCategory.objects.create(
        name=category_name,
        description=description,
        picture=image_name,
        classifiedtype = classifiedType,
        is_active=is_active,
        created_at=date.today(),
        updated_at=date.today()
    )
    
    return redirect("/myadmin/allCategory")

def allCategory(request):
    result = AdCategory.objects.filter(is_active=True)
    context={'result':result}
    return render(request, 'myadmin/allcategory.html', context)
    
def editCategory(request, id):
    result = AdCategory.objects.get(pk=id)
    context = {'result': result}
    return render(request, 'myadmin/editCategory.html', context)
    

def adcategory_update(request, id):
    myimage = request.FILES.get('image')  # Use .get() to avoid KeyError
    # mylocation = os.path.join(settings.MEDIA_ROOT, 'category')
    # obj = FileSystemStorage(location=mylocation)
    
    if myimage:
        mylocation = os.path.join(settings.MEDIA_ROOT, 'category')
        obj = FileSystemStorage(location=mylocation)
        
        # Define the image path
        original_image_path = os.path.join(mylocation, myimage.name)
        
        # Save the original uploaded image
        obj.save(myimage.name, myimage)
        
        # Process the image to remove background
        processed_image_path = os.path.join(mylocation, f"no_bg_{myimage.name}")

        with open(original_image_path, "rb") as input_file:
            image_data = input_file.read()
            output_data = remove(image_data)  # Remove background

        with open(processed_image_path, "wb") as output_file:
            output_file.write(output_data)

        # Use the processed image for storing in DB
        image_name = f"no_bg_{myimage.name}"
    else:
        image_name = None
    # Handle checkbox value safely
    is_active = int(request.POST.get('active', 0)) == 1  # Defaults to 0 if 'active' is missing

    data = {
        "name": request.POST['category_name'],
        "description": request.POST["description"],
        "picture": image_name,  # Save image name or None
        "classifiedtype":request.POST['classifiedtype'].strip(),
        "is_active": is_active
    }

    AdCategory.objects.update_or_create(pk=id, defaults=data)
    return redirect("/myadmin/allCategory")


def adCategoryDelete(request, id):
    res = AdCategory.objects.get(pk=id)
    res.delete()
    return redirect("/myadmin/allCategory")

def nonActiveCategory(request):
    result = AdCategory.objects.filter(is_active=False)
    context={'result':result}
    return render(request, 'myadmin/allcategory.html', context)

def reportLandingPage(request):
    return render(request,'myadmin/report/reportLandingPage.html')

def userReportListing(request):
    return render(request,"myadmin/report/user/userReport.html")

def agencyReportListing(request):
    return render(request,"myadmin/report/agency/agencyReportListing.html")

def trendingReportListing(request):
    return render(request,"myadmin/report/trending/trendingReportListing.html")

def feedbackAndInquiryListing(request):
    return render(request,"myadmin/report/feedbackAndInquiry/feedbackAndInquiryReportListing.html")

def userReport(requset,param):
    param = param.lower()
    if param == "newuser":
        query = """ SELECT u.id, u.username, u.first_name, u.last_name, u.email, p.contact, p.gender, p.address, p.dob, p.profile_image FROM auth_user  as u JOIN profile as p ON p.user_id = u.id WHERE DATE_ADD(u.date_joined,INTERVAL 1 DAY) > CURRENT_TIMESTAMP
        """
        result = User.objects.raw(query)
        context = {'result':result,'type' : param,'reportType' : 'New / Recent Users Report'}
        return render(requset,"myadmin/report/user/report.html",context)
    if param == "activeinactive":
        query = """ SELECT u.id, u.username, u.first_name, u.last_name, u.email, p.contact, p.gender, p.address, p.dob, p.profile_image 
                    FROM auth_user AS u 
                    JOIN profile AS p ON p.user_id = u.id 
                    WHERE u.last_login > DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 MONTH)
        """
        query2 = """ SELECT u.id, u.username, u.first_name, u.last_name, u.email, p.contact, p.gender, p.address, p.dob, p.profile_image FROM auth_user  as u JOIN profile as p ON p.user_id = u.id WHERE u.last_login < DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 MONTH)
        """
        result = User.objects.raw(query)
        
        result2 = User.objects.raw(query2)
        context = {'result':result,'result2':result2,'type' : param,'reportType' : 'Active  Users Report', 'reportType2' : 'Inactive Users Report'}
        return render(requset,"myadmin/report/user/report.html",context)
    
    if param == 'topbuyer':
         query = """SELECT u.id, COUNT(*) as count, p.profile_image, u.username, CONCAT(u.first_name,' ',u.last_name) as fullname FROM `order` as o JOIN auth_user as u ON o.user_id = u.id JOIN profile as p ON p.user_id = u.id GROUP BY u.id
        """
         result = Order.objects.raw(query)
         context = {'result':result,'type':param,'reportType' : "Topbuyer"}
         return render(requset,"myadmin/report/user/report.html",context)
    if param == "blockuser":
        query = """
            SELECT u.id, p.profile_image, u.username, CONCAT(u.first_name," ",u.last_name) as fullname FROM auth_user as u JOIN profile as p ON p.user_id = u.id WHERE u.is_active = 0
        """
        result = Profile.objects.raw(query)
        context = {'result':result,'type':param,'reportType' : "Blocked User"}
        return render(requset,"myadmin/report/user/report.html",context)

def agencyReport(request, param):
    param = param.lower()

    if param == "newagency":
        query = """
        SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
               p.est_date, p.profile_picture 
        FROM agency AS a 
        JOIN agencyprofile AS p ON p.agency_id = a.id 
        JOIN state AS s ON s.id = p.state_id 
        JOIN city AS c ON c.id = p.city_id 
        WHERE DATE_ADD(a.created_at, INTERVAL 1 DAY) > CURRENT_TIMESTAMP
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'New / Recent Agency Report'
        }
        return render(request, "myadmin/report/agency/report.html", context)

    elif param == "activeinactive":
        query_active = """
            SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
                p.est_date, p.profile_picture
            FROM agency AS a 
            JOIN agencyprofile AS p ON p.agency_id = a.id  
            WHERE DATE(a.updated_at) >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        """

        query_inactive = """
            SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
                p.est_date, p.profile_picture 
            FROM agency AS a 
            JOIN agencyprofile AS p ON p.agency_id = a.id 
            WHERE DATE(a.updated_at) <= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        """

        result = Agency.objects.raw(query_active)
        result2 = Agency.objects.raw(query_inactive)

        context = {
            'result': result,
            'result2': result2,
            'type': param,
            'reportType': 'Active Agency Report',
            'reportType2': 'Inactive Agency Report'
        }
        return render(request, "myadmin/report/agency/report.html", context)

    elif param == "notapprove":
        query = """
        SELECT a.id, p.profile_picture, a.username, p.agencyname 
        FROM agency AS a 
        JOIN agencyprofile AS p ON p.agency_id = a.id 
        WHERE a.isBlocked = 0 AND a.approved = 0
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': "Not Approved Agencies"
        }
        return render(request, "myadmin/report/agency/report.html", context)

    elif param == "blockagency":
        query = """
        SELECT a.id, p.profile_picture, a.username, p.agencyname 
        FROM agency AS a 
        JOIN agencyprofile AS p ON p.agency_id = a.id 
        WHERE a.is_blocked = 1
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': "Blocked Agency"
        }
        return render(request, "myadmin/report/agency/report.html", context)
    else:
        return render(request, "myadmin/404.html")

def trendingReport(request, param):
    param = param.lower()
    
    if param == "trendingagency":
        query = """
        SELECT a.id, a.username, a.email, p.agencyname, p.contact, p.address, 
               p.est_date, p.profile_picture, COUNT(o.id) as order_count
        FROM agency AS a
        JOIN agencyprofile AS p ON p.agency_id = a.id
        LEFT JOIN `order` AS o ON o.agency_id = a.id
        WHERE DATE(o.created_at) >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        GROUP BY a.id
        ORDER BY order_count DESC
        LIMIT 10
        """
        result = Agency.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Top Trending Agencies'
        }
        return render(request, "myadmin/report/trending/report.html", context)

    elif param == "trendingcategory":
        query = """
        SELECT c.id, c.name, c.classifiedtype, COUNT(o.id) as order_count,
               RANK() OVER (ORDER BY COUNT(o.id) DESC) as rank
        FROM adcategory AS c
        LEFT JOIN `order` AS o ON o.category_id = c.id
        WHERE DATE(o.created_at) >= DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
        GROUP BY c.id
        ORDER BY order_count DESC
        LIMIT 10
        """
        result = AdCategory.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Top Trending Categories'
        }
        return render(request, "myadmin/report/trending/report.html", context)

    else:
        return render(request, "myadmin/404.html")
    

def feedbackAndInquiryReport(request, param):
    param = param.lower()
    
    if param == "feedback":
        query = """
        SELECT f.id, up.profile_image, u.username, f.rating, f.message, f.created_at
        FROM feedback AS f 
        JOIN auth_user AS u ON u.id = f.user_id 
        JOIN profile AS up ON up.user_id = f.user_id
        ORDER BY f.created_at DESC
        """
        result = User_feedback.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Customer Feedback Report'
        }
        return render(request, "myadmin/report/feedbackAndInquiry/report.html", context)
    
    elif param == "inquiry":
        query = """
        SELECT i.id, i.name, i.email, i.contact, i.message, i.created_at
        FROM inquiry AS i
        ORDER BY i.created_at DESC
        """
        result = Inquiry.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Customer Inquiry Report'
        }
        return render(request, "myadmin/report/feedbackAndInquiry/report.html", context)
    
    elif param == "agencyinquiry":
        query = """
        SELECT i.id, i.agency_id, a.username as agency, u.username as user, i.subject, i.message, i.created_at
        FROM agency_inquiry AS i 
        JOIN agency AS a ON a.id = i.agency_id
        JOIN auth_user AS u ON u.id = i.user_id
        ORDER BY i.created_at DESC
        """
        result = Inquiry.objects.raw(query)
        context = {
            'result': result,
            'type': param,
            'reportType': 'Customer Inquiry Report'
        }
        return render(request, "myadmin/report/feedbackAndInquiry/report.html", context)
    
    else:
        return render(request, "myadmin/404.html")
