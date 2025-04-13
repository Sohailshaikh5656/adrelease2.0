"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from customer import views

urlpatterns = [

    path('home', views.home, name='home'),
    path('', views.login, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('ForgetPassword', views.ForgetPassword, name='ForgetPassword'),
    path('ForgetPassword_chk', views.ForgetPassword_chk, name='ForgetPassword_chk'),
    path('ChangePassword', views.ChangePassword, name='ChangePassword'),
    path('ChangePassword_chk', views.ChangePassword_chk, name='ChangePassword_chk'),

     # path('change_password', views.change_password, name='change_password'),
    path('register', views.register, name='register'),
    path('user_store', views.user_store, name='user_store'),
    path('contactus', views.contactus, name='contactus'),
    path('store_cust_inquiry', views.store_cust_inquiry, name='store_cust_inquiry'),

    path('agency', views.agency, name='agency'),
    path('agency_register', views.agency_register, name='agency_register'),
    path('agency_store', views.agency_store, name='agency_store'),
    path('agency_login_check', views.agency_login_check, name='agency_login_check'),


    path('aboutus', views.aboutus, name='aboutus'),

    path('feedback', views.feedback, name='feedback'),
    path('store_cust_feedback', views.store_cust_feedback, name='store_cust_feedback'),
    

    path('logout', views.logout, name='logout'),


    path('post_advertisement', views.post_advertisement, name='post_advertisement'),
    path('search_advertisement', views.search_advertisement, name='search_advertisement'),
    
    path('search_advertise', views.search_advertise, name='search_advertise'),
    path('ordersummary/<str:type>', views.ordersummary, name='ordersummary'),
    path('order_delete/<int:id>', views.order_delete, name='order_delete'),
    # path('place_order/<int:id>', views.place_order, name='place_order'),
    path('order_store/<int:id>', views.order_store, name='order_store'),
   
    path('customer_order/<int:id>', views.customer_order, name='customer_order'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('userprofile/<int:id>', views.userprofile, name='userprofile'),
    path('userprofile_update/<int:id>', views.userprofile_update, name='userprofile_update'),
   
    path('profile_image/<int:id>', views.profile_image, name='profile_image'),
    path('Agency_ForgetPassword', views.Agency_ForgetPassword, name='Agency_ForgetPassword'),
    path('Agency_ForgetPassword_chk', views.Agency_ForgetPassword_chk, name='Agency_ForgetPassword_chk'),
    path('payment', views.payment, name='payment'),
    path('process_payment', views.process_payment, name='process_payment'),
    path('success/<int:id>', views.success, name='success'),
    
    path('custom_404_view', views.custom_404_view, name='custom_404_view'),
    path('singleAdType/<int:id>', views.singleAdType, name = 'singleAdType'),
    
    #==========================Diffrent Order Page : ======================

    path('order/classifiedTextAdOrderPage/<int:id>', views.classifiedTextAdOrderPage, name = 'classifiedTextAdOrderPage'),
    path('SelectRegion/<int:id>', views.SelectRegion, name = 'SelectRegion'),
    path('get-cities/', views.get_cities, name='get_cities'), # AJAX Endpoint 
    path('SelectedRegion', views.SelectedRegion, name='SelectedRegion'),
    path('textOrderStore', views.textOrderStore, name='textOrderStore'),
    path('send_test_email_view', views.send_test_email_view, name='send_test_email_view'),
    path('chat_with_bot/', views.chat_with_bot, name='chat_with_bot'),
    path('agencyInquiry', views.agencyInquiry, name='agencyInquiry'),
    path('store_agency_inquiry', views.store_agency_inquiry, name='store_agency_inquiry'),
]
