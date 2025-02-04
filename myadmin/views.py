from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .approve import send_mail_to_user
from .reject import send_mail_of_reject
from django.core.mail import send_mail
import os
from django.core.exceptions import ObjectDoesNotExist
from .helper1 import send_forget_password_mail
from django.http import HttpResponse
from django.views.generic import View
from .helpers import html_to_pdf 


class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        query = request.user.id
        result = Order.objects.all()
        context = {'result':result}
        # getting the template
        pdf = html_to_pdf('pdf.html',context)
        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

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
    result = Order.objects.get(pk=id)
    context = {'result':result}
    return render(request,'myadmin/order_viewmore.html',context)

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
        SELECT ap.agencyname,ap.city, ap.state, a.email, a.username, a.id as id from agency as a JOIN agencyprofile as ap ON ap.agency_id = a.id WHERE
        approved = 0 AND isBlocked = 0 AND isactive = 1  
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
    SELECT a.id as id, ap.agencyname, ap.city, ap.state, a.email, a.username
    FROM agency as a
    JOIN agencyprofile as ap ON ap.agency_id = a.id
    WHERE a.approved = 1 AND a.isBlocked = 1 AND a.isactive = 1
"""


    result = Agency.objects.raw(query)
    context = {'result':result}
    return render(request,'myadmin/showAllBlockAgency.html',context)

def agency_block_process(request,id):
    result = Agency.objects.get(pk=id)
    result.isBlocked = 1
    result.save()
    return redirect('/myadmin/blocked_Agency')

def unblocked_Agency(request):
    query = """
        SELECT ap.agencyname,ap.city, ap.state, a.email, a.username, a.id as id from agency as a JOIN agencyprofile as ap ON ap.agency_id = a.id WHERE
        approved = 1 AND isBlocked = 1 AND isactive = 1  
    """
    result = Agency.objects.raw(query)
    context = {'result':result}
    return render(request,'myadmin/agency_Unblock.html',context)

def agency_unblock_process(request,id):
    result = Agency.objects.get(pk=id)
    result.isBlocked = 0
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
    result.save()
    return redirect('/myadmin/customer')