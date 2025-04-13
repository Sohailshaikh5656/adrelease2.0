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
from django.http import JsonResponse
from .utils import *
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def home(request):
    request.session.setdefault('visitor_count', 0)
    request.session['visitor_count'] += 1
    adCategory = AdCategory.objects.filter(classifiedtype__icontains="Classified Text Ad")
    adCategory2 = AdCategory.objects.filter(classifiedtype="Classified Display Ad")
    adCategory3 = AdCategory.objects.filter(classifiedtype="Display Ad")


    id = request.user.id
    if id == None:
        result1 = Newadtype.objects.all()
        context = {'result1':result1,'adCategory': adCategory,
                    'adCategory2':adCategory2,'adCategory3':adCategory3}

        return render (request,'customer/home.html',context)
    else:
        result = User.objects.get(pk=id)
        result1 = Newadtype.objects.all()
        feedback = User_feedback.objects.all()
        context = {'result': result, 'feedback': feedback, 'result1': result1, 'adCategory': adCategory,
                    'adCategory2':adCategory2,'adCategory3':adCategory3
        }
        print(adCategory)
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
            request.session["user_id"] = result1.id
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


    if result is None:
        messages.success(request, 'Invalid Username ')
        print('Invalid Username Or Password')
        return redirect('/customer/ForgetPassword')

    else:
        email = result.email
        fname = result.first_name
        lname = result.last_name

        
        insertedUsername = result.username  
        insertedEmail = result.email

        import secrets
        import string
        from datetime import datetime, timedelta
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20))
        print("Token Generated : ",token)
        from customer.models import ForgetPassword
        expiry_time = datetime.now() + timedelta(minutes=10)
        ForgetPassword.objects.create(username=insertedUsername, email=insertedEmail, token=token, expiry_date_time=expiry_time)
        send_password_reset_email(email,fname+" "+ lname,token)
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
        send_welcome_email(result)
        return redirect('/customer/')

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
    send_inquiry_received_email(name,contact,email,message)
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
        
        if result is None:
            messages.success(request, 'Invalid Username or Username Not Found')
            return redirect('/customer/agency')
        elif result.approved==False:
            messages.success(request, 'Wait For Approval Account')
            return redirect('/customer/agency')
        elif result.isBlocked == True:
            messages.success(request, 'Your Account Has Been Blocked!')
            return redirect('/customer/agency')
        elif result.password == password:  # Direct password comparison
            request.session['agency_id'] = result.id 
            request.session['super_agency_id'] = result.id # Set agency_id in session
            return redirect('/agency/dashboard')
        else:
            messages.success(request, 'Invalid Password')
            return redirect('/customer/agency')
    except ObjectDoesNotExist:
         messages.success(request, 'Invalid Username or You are not Agency')
         return redirect('/customer/agency')


def agency_register(request):
    state = State.objects.all()
    context = {'state':state}
    return render(request,'customer/agency_register.html', context)

def agency_store(request):
    try:
        # Get file if it exists
        if 'profile_picture' in request.FILES:
            myfile = request.FILES['profile_picture']
            mylocation = os.path.join(settings.MEDIA_ROOT,'profile')
            obj = FileSystemStorage(location=mylocation)
            filename = obj.save(myfile.name, myfile)
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['pass']
            cpassword = request.POST['cpass']

            # Agency_Profile Model
            agencyname = request.POST['agencyname']
            ownername = request.POST['ownername']
            contact = request.POST['contactno']
            address = request.POST['address']
            city_id = request.POST['city']  # Changed 'city' to 'city_id'
            state_id = request.POST['state']  # Changed 'state' to 'state_id'
            est_date = request.POST['est_date']
            per_word_rate = request.POST['per_word_rate']
            circulation = request.POST['circulation']
            cm_charge = request.POST['cm_charge']

            if password == cpassword:
                agency = Agency.objects.create(
                    email=email,
                    username=username,
                    password=password,
                    created_at=datetime.today(),
                    updated_at=datetime.today()
                    # Call the method here
                )

                print("Agency ID:", agency.id)
                print("Agency Name:", agencyname)
                print("Owner Name:", ownername)
                print("Contact:", contact)
                print("Address:", address)
                print("City ID:", city_id)  # Print city_id
                print("State ID:", state_id  ) # Print state_id
                print("Est Date:", est_date)
                print("Per Word Rate:", per_word_rate)
                print("Circulation:", circulation)
                print("Profile Picture:", filename)

                # Get the City and State objects
                city = City.objects.get(pk=city_id)
                state = State.objects.get(pk=state_id)

                Agencyprofile.objects.create(
                    agencyname=agencyname,
                    ownername=ownername,
                    contact=contact,
                    address=address,
                    city=city,
                    state=state,
                    est_date=est_date,
                    per_word_rate=per_word_rate,
                    circulation=circulation,
                    profile_picture=filename,
                    agency=agency,
                    cm_charge = cm_charge
                )

                # Passwordall.objects.create(password_user=password, user_id=result.id)
                messages.success(request, 'Successfully Registered. Login to Access.')
                return redirect('/customer/agency_register')
            else:
                messages.error(request, 'Password Mismatch')
                return redirect('/customer/agency_register')

        else:
            # Handle case where no file was uploaded
            messages.error(request, 'Please upload a profile picture')
            return redirect('/customer/agency_register')
    except Exception as e:
        messages.error(request, f'Error during registration: {str(e)}')
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



def ordersummary(request, type):
    user = request.user.id
    result = None
    
    if type == 'all':
        result = Order.objects.filter(user_id=user)
    elif type == "newOrder":
        result = Order.objects.filter(user_id=user, is_approve=0)
    elif type == "approved":
        result = Order.objects.filter(user_id=user, is_approve=1)
    elif type == "history":
        result = Order.objects.filter(user_id=user, is_printed=1)
    
    
    context = {'result': result}
    return render(request, 'customer/ordersummary.html', context)

def order_delete(request,id):
    result = Order.objects.get(pk=id)
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
    amount = int(request.session['total_price']) * 100
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

#======================= Different Orders =====================================

def classifiedTextAdOrderPage(request, id):
    request.session['agencyOrderId'] = id
    AdCategory_id = request.session['adCategory_id']
    print(AdCategory_id)
    AdClassification = AdCategory.objects.get(pk=AdCategory_id)
    if(AdClassification.classifiedtype == 'Classified Text Ad'):
        result = Agencyprofile.objects.get(agency_id=id)
        context = {'result':result}
        return render(request, 'customer/orderPage/ClassifiedTextAdOrder.html',context)
    elif(AdClassification.classifiedtype == 'Classified Display Ad'):
        result = Agencyprofile.objects.get(agency_id=id)
        context = {'result':result}
        return render(request, 'customer/orderPage/ClassifiedDisplayAdOrder.html',context)
    elif(AdClassification.classifiedtype == "Display Ad"):
        result = Agencyprofile.objects.get(agency_id=id)
        context = {'result':result}
        return render(request, 'customer/orderPage/DisplayAdOrder.html',context)

    
# def SelectRegion(request):
#     return render(request, 'customer/regionSelect.html')

def SelectRegion(request,id):
    request.session['adCategory_id'] = id
    print('AdCategory_id : ',id)
    states = State.objects.filter(is_active=True, is_deleted=False).order_by('state_name')
    return render(request, 'customer/regionSelect.html', {'states': states})

def get_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id, is_active=True, is_deleted=False).values('id', 'city_name')
    return JsonResponse({'cities': list(cities)})

from django.http import JsonResponse
from .models import AgencyRegion, Agency

def SelectedRegion(request):
    if request.method == "POST":
        city_id = request.POST.get('city')  # Get city ID from request
        cityResult = City.objects.get(pk=city_id);
        cat_id = request.session.get('adCategory_id')
        
        if not city_id or not cat_id:
            return JsonResponse({"error": "Missing city or category ID"}, status=400)

        try:
            AdClassification = AdCategory.objects.get(pk=cat_id)
        except AdCategory.DoesNotExist:
            return JsonResponse({"error": "Invalid ad category ID"}, status=400)

        query = '''SELECT a.id, ap.agencyname, ap.circulation, ap.per_word_rate, a.username, ap.profile_picture, ap.cm_charge,
        (SELECT GROUP_CONCAT(c.city_name) FROM city as c JOIN agencyregion as ar ON ar.agency_id = a.id WHERE ar.state_id = %s and ar.city_id = c.id) as regions
        FROM agency as a JOIN agencyregion as ar ON ar.agency_id = a.id JOIN agencyprofile as ap ON a.id = ap.agency_id WHERE a.approved=1 AND a.isBlocked=0 AND ar.city_id = %s'''
        result = AgencyRegion.objects.raw(query, [cityResult.state_id,city_id])
        print(result)

        if(AdClassification.classifiedtype == 'Classified Text Ad'):
            adType = "adType1"
        elif(AdClassification.classifiedtype == 'Classified Display Ad'):
            adType = "adType2"
        elif(AdClassification.classifiedtype == "Display Ad"):
            adType = "adType3"
        else:
            return JsonResponse({"error": "Invalid classified type"}, status=400)

        context={'result':result,'adType' : adType}
        return render(request,'customer/selectAgency.html',context)
    return JsonResponse({"error": "Invalid request method"}, status=400)  # Handle non-POST requests
def textOrderStore(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        advertiseImage = request.FILES.get('advertiseImage')
        height = request.POST.get('height')
        width = request.POST.get('width')
        ad_color = request.POST.get('adcolor')
        any_preferance = request.POST.get('anypreferance')
        
        poster_name = None
        if advertiseImage:
            try:
                mylocation = os.path.join(settings.MEDIA_ROOT, 'order')
                fs = FileSystemStorage(location=mylocation)
                name = fs.save(advertiseImage.name, advertiseImage)
                poster_name = name  # Store the saved file name
            except Exception as e:
                messages.error(request, f"Error saving image: {e}")
                return HttpResponse(f"Error saving image: {e}")

        total_price = request.POST.get('total_price', '0').strip()
        try:
            total_price = int(float(total_price)) if total_price else 0
        except ValueError:
            messages.error(request, "Invalid total price format.")
            return HttpResponse("Invalid total price format.")

        agencyOrderId = request.session.get('agencyOrderId')
        adCategory = request.session.get('adCategory_id')
        request.session['total_price'] = total_price
        
        print(f"Total price received: {total_price}")

        try:
            order = Order.objects.create(
                agency_id=agencyOrderId,
                date=date,
                subject=subject,
                description=description if description else None,
                height=height if height else None,
                width=width if width else None,
                price=total_price,
                user_id=request.user.id,
                poster=poster_name,  # Use the stored file name or None
                category_id=adCategory,
                ad_color=ad_color,
                any_preferance=any_preferance if any_preferance else None
            )
            user = User.objects.get(pk=order.user_id)
            agency = Agency.objects.get(pk=order.agency_id)
            messages.success(request, "Order placed successfully!")
            send_order_confirmation_email(user,order,agency)
            return redirect("/customer/process_payment")
        except Exception as e:
            messages.error(request, f"Error placing order: {e}")
            return HttpResponse(f"Error placing order: {e}")
    else:
        return HttpResponse("Invalid request method.")
    
def send_test_email_view(request):  # Note the 'request' parameter
    send_test_email()  # This calls our utility function
    return HttpResponse("Test email sent successfully! Check your console.")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import logging

# Configure logger
logger = logging.getLogger(__name__)


# Replace with your Gemini API key
GEMINI_API_KEY = "AIzaSyDSEV3aFXyca6Atd9ygEvJkeIGmpvBV3w8"

@csrf_exempt
def chat_with_bot(request):
    if request.method == "POST":
        try:
            # Log the incoming request data
            data = json.loads(request.body)
            user_message = data.get("message", "")
            logger.info(f"Received message from user: {user_message}")

            # Prepare the Gemini API request data
            gemini_payload = {
                "contents": [{
                    "parts": [{"text": user_message}]
                }]
            }

            # Call Gemini API for response
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
                json=gemini_payload,
                headers={'Content-Type': 'application/json'}
            )
            print(response)
            # Check if the response was successful (status code 200)
            if response.status_code == 200:
                gemini_response = response.json()

                # Log the full Gemini response to see its structure
                logger.info(f"Gemini API Response: {gemini_response}")

                # Inspect the actual content in the response (Gemini content structure)
                # Check if the key "content" exists in the response
                bot_reply = gemini_response.get("content", "Sorry, I couldn't get a response.")

                return JsonResponse({"response": bot_reply})

            else:
                # Log the error with the status code
                logger.error(f"Gemini API request failed with status code: {response.status_code}")
                return JsonResponse({"error": "Gemini API request failed"}, status=500)

        except Exception as e:
            logger.error(f"Error: {str(e)}")  # Log any errors
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


def agencyInquiry(request):
    agencies = Agency.objects.all()
    context = {'agencies': agencies}
    return render(request, 'customer/agencyInquiry.html', context)

def store_agency_inquiry(request):
    if request.method == 'POST':
        try:
            agency_id = request.POST.get('agency_id')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            user_id = request.session.get('user_id')

            agency = Agency.objects.get(id=agency_id)
            user = User.objects.get(id=user_id)

            AgencyInquiry.objects.create(
                agency=agency,
                subject=subject,
                message=message,
                user=user
            )
            messages.success(request, 'Your inquiry has been submitted successfully')
            return redirect('/customer/agencyInquiry')

        except Exception as e:
            messages.error(request, f'Error submitting inquiry: {str(e)}')
            return redirect('/customer/agencyInquiry')
    else:
        return redirect('/customer/agencyInquiry')
