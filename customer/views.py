from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from customer.models import *
from agency.models import *
from django.core.mail import send_mail
import uuid
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from datetime import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .helper import send_forget_password_mail
from .agencyhelper import send_forget_password_mail_to_agency
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone 

# Create your views here.
def home(request):
    request.session.setdefault('visitor_count', 0)
    request.session['visitor_count'] += 1


    id = request.user.id
    if id == None:
        result1 = Newadtype.objects.all()
        context = {'result1':result1}

        return render (request,'customer/home.html',context)
    else:
        result = User.objects.get(pk=id)
        result1 = Newadtype.objects.all()
        feedback = User_feedback.objects.all()
        context={'result':result, 'feedback':feedback, 'result1':result1 }
        return render (request,'customer/home.html',context)
#---------------------------------------------------------------

def logout(request):
    auth.logout(request)
    return redirect('/customer')
#---------------------------------------------------------------

def login(request):
    context={}
    return render (request,'customer/login.html',context)

def login_check(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        result1 = User.objects.get(username=username)
        result = auth.authenticate(request, username=username,password=password)
        if result1.first_name == "" or result1.is_staff != 0:
            messages.success(request, 'Invalid Username Or Password or You are Not Authorised User !!')
            print('Invalid Username Or Password or You are Not Authorised User')
            return redirect('/customer')
        if result is None:
            messages.success(request, 'Invalid Username or Password')
            print('Invalid Username or Password')
            return redirect('/customer/')
        else:
            auth.login(request, result)
            return redirect('/customer/home')

    except ObjectDoesNotExist:
         my_object = None
         messages.success(request, 'Invalid Username or not Found Username')
         print('Invalid Username or You are not Admin')
         return redirect('/customer/')
#---------------------------------------------------------------

def ChangePassword_chk(request):
    user_id = request.user.id
    username = request.POST['currentpass']
    passwd = request.POST['pass']
    cpasswd = request.POST['cpass']

    if passwd != cpasswd:
        messages.success(request, 'Confirm password does not match')
        return redirect('/customer/ChangePassword')
    if user_id is None:
        messages.success(request, 'Login First to Change Password')
        return redirect('/customer/')

    else :
        u= User.objects.get(username=username)
        u.set_password(passwd)
        u.save()
        data = {
                'password_user': passwd
                }
        Passwordall.objects.update_or_create(user_id=user_id, defaults=data)
        messages.success(request, 'Successfully Updated !! \nlogin first')
        return redirect('/customer/')


def ChangePassword(request):
    return render(request,'customer/ChangePassword.html')


def ForgetPassword(request):

    
    return render(request,'customer/forgotpassword.html')


def ForgetPassword_chk(request):

    username = request.POST['username']
    result = User.objects.get(username=username)
    user_id = result.id
    result1 = Passwordall.objects.get(user_id = user_id)

    if result is None:
        messages.success(request, 'Invalid Username ')
        print('Invalid Username Or Password')
        return redirect('/customer/ForgetPassword')

    else:
        email = result.email
        fname = result.first_name
        lname = result.last_name
        password = result1.password_user
        
        send_forget_password_mail(email,password,fname,lname)
        messages.success(request, 'Check Your Mail ')
    
    
    return redirect('/customer/ForgetPassword')
    

def Agency_ForgetPassword(request):

    
    return render(request,'customer/agencyforgetpassword.html')


def Agency_ForgetPassword_chk(request):

    username = request.POST['username']
    result = User.objects.get(username=username)
    user_id = result.id
    result1 = Passwordall.objects.get(user_id = user_id)

    if result is None:
        messages.success(request, 'Invalid Username ')
        print('Invalid Username Or Password')
        return redirect('/customer/ForgetPassword')

    else:
        email = result.email
        
        username = result.username
        password = result1.password_user
        
        send_forget_password_mail_to_agency(email,password,username)
        messages.success(request, 'Check Your Mail ')
    
    
    return redirect('/customer/Agency_ForgetPassword')
    



def register(request):
    context={}
    return render (request,'customer/registar.html',context)


def user_store(request):
    # User Model

    fname = request.POST['fname']
    lname = request.POST['lname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['pass']
    cpassword = request.POST['cpass']

    # Profile Model
    contact = request.POST['contactno']
    gender = request.POST['gender']
    address = request.POST['address']
    dob = request.POST['dob']

    if password == cpassword:
        result = User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
        Profile.objects.create(contact=contact,gender=gender,address=address,dob=dob,user_id=result.id)
        Passwordall.objects.create(password_user = password,user_id=result.id)
        messages.success(request, 'Account Created Successfully !! \nPlease Login !! ')
        return redirect('/customer/')
        send_mail(
            'Forget Password',
            'Click Here To Reset Password http://127.0.0.1:8000/customer/ChangePassword',
            'shaikhsohail1131@gmail.com',
            [email],
            fail_silently=False,
            )
        
    
        

    else:
        messages.success(request, 'Password Missmatch')
        print("Missmatch Password")
        return redirect('/customer/register')




#---------------------------------------------------------------
# def cust_registar_store(request):
#     # User Model
#     fname     = request.POST['fname']
#     lname     = request.POST['lname']
#     email     = request.POST['email']
#     username  = request.POST['username']
#     password  = request.POST['password']
#     cpassword = request.POST['cpassword']

#     # Profile Model
#     contact = request.POST['contact']
#     address = request.POST['address']

#     if password == cpassword:
#         result = User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
#         Profile.objects.create(contact=contact,address=address,user_id=result.id)
#         return redirect('/account/register')
#     else:
#         print('Missmatch Password')


def contactus(request):
    context={}
    return render (request,'customer/contactus.html',context)

def store_cust_inquiry(request):
    name = request.POST['name']
    email = request.POST['email']
    contact = request.POST['contact']
    message = request.POST['message']
    

    Inquiry.objects.create(name=name, email=email, contact=contact, message=message)
    messages.success(request, 'Inquiry Send')

    return redirect('/customer/contactus')

#-----------Agency_login,Agency_Register-----------

def agency(request):
    agency = User.objects.all()
    context={'agency':agency}
    return render(request,'customer/agencylogin.html',context)

def agency_login_check(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        result = Agency.objects.get(username=username)
        # result = auth.authenticate(request, username=username,password=password)
        
        if result is None:
            messages.success(request, 'Invalid Username or Username Not Found')
            print('Invalid Username or You are not Admin')
            return redirect('/customer/agency')
        elif result.approved==False:
            messages.success(request, 'Wait For Approval Account')
            print('Invalid Username or You are not Admin')
            return redirect('/customer/agency')
        elif result.isBlocked == True:
            messages.success(request, 'Your Account Has Been Blocked !')
            print('Invalid Username or You are not Admin')
            return redirect('/customer/agency')
        elif result.username == username and result.password == password:
            request.session['super_agency_id'] = result.id
            return redirect('/agency/dashboard')
        else:
            messages.success(request, 'Something Went Wrong !')
            print('Something Went Wrong !')
            return redirect('/customer/agency')
    except ObjectDoesNotExist:
         my_object = None
         messages.success(request, 'Invalid Username or You are not Agency')
         print('Invalid Username or You are not Admin')
         return redirect('/customer/agency')



def agency_register(request):

    return render(request,'customer/agency_register.html')

def agency_store(request):
    email     = request.POST['email']
    username  = request.POST['username']
    password  = request.POST['pass']
    cpassword = request.POST['cpass']

    # Agency_Profile Model
    agencyname = request.POST['agencyname']
    ownername  = request.POST['ownername']
    contact    = request.POST['contactno']
    address    = request.POST['address']
    city       = request.POST['city']
    state      = request.POST['state']
    est_date   = request.POST['est_date']
    
    if password == cpassword:
        result = Agency.objects.create(
            email=email,
            username=username,
            password=password,
            created_at=datetime.today(),
            updated_at = datetime.today()
                # Call the method here
        )
        
        Agencyprofile.objects.create(
            agencyname=agencyname,
            ownername=ownername,
            contact=contact,
            address=address,
            city=city,
            state=state,
            est_date=est_date,
            agency_id=result.id
        )

        # Passwordall.objects.create(password_user=password, user_id=result.id)
        messages.success(request, 'Successfully Registered. Login to Access.')
        return redirect('/customer/agency_register')
    else:
        messages.error(request, 'Password Mismatch')
        return redirect('/customer/agency_register')
#----------------------------------------------------------------


def aboutus(request):
    context={}
    return render(request,'customer/aboutus.html',context)

#------------------------------------------------------------------
def feedback(request):
    context={}
    return render(request,'customer/feedback.html',context)

def store_cust_feedback(request):
    rating  = request.POST['rating']
    message = request.POST['message']
    id = request.user.id
    User_feedback.objects.create(rating=rating,message=message,user_id=id)
    return redirect('/customer/feedback')
    messages.success(request, 'Thanks Of Feedback')



def post_advertisement(request):
    context={}
    return render(request,'customer/post_advertisment.html',context)

# def search_advertisement(request):
#   size = request.POST['size']
#   page = request.POST['pageno']
#   mode = request.POST['mode']
#   result = Newadtype.objects.all()


#   if size == result.size and page == result.pageno and mode == result.adtype:
#       result1 = 


def search_advertise(request):
    size   = request.POST['size']
    pageno = request.POST['pageno']
    mode   = request.POST['mode']

    request.session['size']   = size
    request.session['pageno'] = pageno
    request.session['mode']   = mode

    result = Newadtype.objects.filter(size=size,pageno=pageno,adtype=mode)
    context={'result':result}
    return render(request,'customer/search_advertise.html',context)

# def place_order(request,id):
#   context={}
#   return render(request,'customer/order.html',context)
from django.utils import timezone  # ✅ Correct import

def order_store(request, id):
    myimage = request.FILES['image']
    myword = request.FILES['word']
    mylocation = os.path.join(settings.MEDIA_ROOT, 'order')
    obj = FileSystemStorage(location=mylocation)
    obj.save(myimage.name, myimage)
    obj.save(myword.name, myword)

    result = Newadtype.objects.get(pk=id)
    size = request.session.get('size')
    pageno = request.session.get('pageno')
    mode = request.session.get('mode')
    date = request.POST['date']
    subject = request.POST['subject']
    description = request.POST['description']
    user = request.user.id
    ad_id = request.session.get('ad_id')
    agency = int(request.session.get('agency_id', 0))  # Convert to int

    # Debugging prints
    print(f"Session ad_id: {ad_id} (Type: {type(ad_id)})")

    if not ad_id:
        messages.error(request, "Ad Type ID is missing.")
        return redirect('/customer/some_page')

    try:
        ad_id = int(ad_id)  # Ensure ad_id is an integer
        ad_type_obj = Newadtype.objects.get(id=ad_id)  # Fetch object
    except ValueError:
        messages.error(request, "Invalid Ad Type ID format.")
        return redirect('/customer/some_page')
    except Newadtype.DoesNotExist:
        messages.error(request, "Ad Type ID does not exist.")
        return redirect('/customer/some_page')

    price = result.price
    res1 = Order.objects.create(
        adType=ad_type_obj,  # ✅ Use ForeignKey object
        size=size, pageno=pageno, mode=mode,
        order_date=timezone.now().date(),  # ✅ Fix timezone usage
        date=date, subject=subject, description=description, price=price,
        user_id=user, agency_id=agency, poster=myimage.name, word=myword.name
    )
    Payment.objects.create(amount=price, agency_id=agency, adType=ad_type_obj,user_id=user,order_id = res1)
    return redirect('/customer/process_payment')

    # myimage = request.FILES['image']
    # myword = request.FILES['word']
    # mylocation = os.path.join(settings.MEDIA_ROOT, 'order')
    # obj = FileSystemStorage(location=mylocation)
    # obj.save(myimage.name, myimage)
    # obj.save(myword.name, myword)

    # result = Newadtype.objects.get(pk=id)
    # size = request.session.get('size')
    # pageno = request.session.get('pageno')
    # mode = request.session.get('mode')
    # date = request.POST['date']
    # subject = request.POST['subject']
    # description = request.POST['description']
    # user = request.user.id
    # ad_id = request.session.get('ad_id')
    # agency = int(request.session.get('agency_id', 0))  # Convert to int

    # # Debugging prints
    # print(f"Session ad_id: {ad_id} (Type: {type(ad_id)})")

    # if not ad_id:
    #     messages.error(request, "Ad Type ID is missing.")
    #     return redirect('/customer/some_page')

    # try:
    #     ad_id = int(ad_id)  # Ensure ad_id is an integer
    #     ad_type_obj = Newadtype.objects.get(id=ad_id)  # Fetch object
    # except ValueError:
    #     messages.error(request, "Invalid Ad Type ID format.")
    #     return redirect('/customer/some_page')
    # except Newadtype.DoesNotExist:
    #     messages.error(request, "Ad Type ID does not exist.")
    #     return redirect('/customer/some_page')

    # price = result.price
    # #Payment.objects.create(amount=price, agency_id=agency, user_id=user)
    # Order.objects.create(
    #     adType=ad_type_obj,  # ✅ Use ForeignKey object
    #     size=size, pageno=pageno, mode=mode,
    #     order_date=timezone.now().date(),  # ✅ Add missing field
    #     date=date, subject=subject, description=description, price=price,
    #     user_id=user, agency_id=agency, poster=myimage.name, word=myword.name
    # )

    # return redirect('/customer/process_payment')

    
    
#--------------------user profile---------------------
import json
def customer_order(request, id):
    result = Newadtype.objects.get(pk=id)
    agency_id = result.agency_id
    price = result.price

    # Fetch all booked order dates for this adType
    order_dates = Order.objects.filter(adType_id=result.id).values_list('date', flat=True)
    order_dates = [date.strftime('%Y-%m-%d') for date in order_dates]  # Convert to string format

    request.session['ad_id'] = result.id
    request.session['agency_id'] = agency_id
    request.session['price'] = price
    print(order_dates)

    context = {
        'result': result,
        'order_dates': json.dumps(order_dates)  # Pass booked dates to template
    }
    return render(request, 'customer/customer_order.html', context)


def userprofile(request,id):
    fkid = request.user.id
    result = User.objects.get(pk=id)
    result1 = Profile.objects.get(user_id = fkid)
    context = {'result1':result1}
    return render(request,'customer/userprofile.html',context)

    
        
def profile(request,id):
    try:
        fkid = request.user.id
        result = User.objects.get(pk=id)
        result1 = Profile.objects.get(user_id = fkid)
        context = {'result1':result1}
        return render(request,'customer/profile.html',context)

    except Profile.DoesNotExist:
        messages.success(request, 'You Are Not Authorized User')
        return redirect("/customer/home")

    


def userprofile_update(request,id):
    user = request.user.id
    result = Profile.objects.get(pk=id)

    data = {
                'fname': request.POST['fname'],
                'lname': request.POST['lname'],
                'email': request.POST['email'],
                'username': request.POST['username']

            }

    data1 = {
                'contactno': request.POST['contactno'],
                'address': request.POST['address'],
                
                'dob': request.POST['dob'],
                'gender': request.POST['gender']

    }

    result = User.objects.update_or_create(pk=user, defaults=data)
    Profile.objects.update_or_create(pk=id, defaults=data1)
    return redirect('/customer/home')



def ordersummary(request):
    user = request.user.id
    result = Order_approve.objects.filter(user_id=user)
    context ={'result':result}
    return render(request,'customer/ordersummary.html',context)

def order_delete(request,id):
    result = Order_approve.objects.get(pk=id)
    result.delete()
    return redirect('/customer/ordersummary')
def search_advertisement(request):
    search = request.POST['search']

    lookup = (Q(adtype__icontains=search) | Q(size__icontains=search) | Q(description__icontains=search) | Q(title__icontains=search))
    
    result1 = Newadtype.objects.filter(lookup)
    
    context={'feedback':feedback, 'result1':result1}
    return render (request,'customer/home.html',context)
    







    
    
def profile_image(request, id):
    user = request.user.id
    result2 = Profile.objects.get(user_id=user)
    myfile = request.FILES['f']
    mylocation = os.path.join(settings.MEDIA_ROOT,'profile')
    obj = FileSystemStorage(location=mylocation)
    obj.save(myfile.name, myfile)

    data = {
            'profile_image' : myfile.name
    }
    Profile.objects.update_or_create(user_id=user, defaults=data )
    fkid = request.user.id
    result = User.objects.get(pk=id)
    result1 = Profile.objects.get(user_id = fkid)
    context = {'result1':result1}
    return render(request,'customer/profile.html',context)

def payment(request):
    context = {}
    return render(request,'customer/payment.html',context)

@csrf_exempt
def success(request,id):
    return render(request, "customer/success.html")

def process_payment(request):
    
    key_id = 'rzp_test_QNjv8QlCmwSAy1'
    key_secret = 'ZPfmqY4Y21JBquMOkBl90mTh'
    amount = int(request.session['price']) * 100
    client = razorpay.Client(auth=(key_id, key_secret))
    data = {
        'amount': amount,
        'currency': 'INR',
        "receipt":"OIBP",
        "notes":{
            'name' : 'AK',
            'payment_for':'OIBP Test'
        }
    }

    id = request.user.id
    result = User.objects.get(pk=id)
    payment = client.order.create(data=data)
    context = {'payment' : payment,'result':result,}
    return render(request, 'customer/payment.html',context)
    
def profile_image(request,id):
    user = request.user.id
    result = Profile.objects.get(user_id=user)
    myfile = request.FILES['f']
    mylocation = os.path.join(settings.MEDIA_ROOT,'profile')
    obj = FileSystemStorage(location=mylocation)
    obj.save(myfile.name, myfile)

    data = {
            'profile_image' : myfile.name
    }
    Profile.objects.update_or_create(user_id=user, defaults=data )
    return redirect('/customer/home')

def custom_404_view(request, exception):
    return redirect('/customer/')

def singleAdType(request,id):
    result = Newadtype.objects.get(pk=id)
    result2 = Agencyprofile.objects.get(agency_id= result.agency_id)
    result3 = Newadtype.objects.filter(agency_id = result.agency_id)
    context = {
        'result':result,
        'result2':result2,
        'result3':result3,
    }

    return render(request,'customer/singleAdType.html',context)

