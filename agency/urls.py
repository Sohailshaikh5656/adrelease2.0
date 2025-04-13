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
from agency import views

from .views import *

urlpatterns = [
    path('pdf/', GeneratePdf.as_view()),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('agency_inquiry', views.agency_inquiry, name='agency_inquiry'),
    path('feedback', views.feedback, name='feedback'),
    path('', views.login, name='login'),
    path('add_agency', views.add_agency, name='add_agency'),
    path('order', views.order, name='order'),
    path('order_viewmore/<int:id>', views.order_viewmore, name='order_viewmore'),
    path('payment', views.payment, name='payment'),
    path('agency_inquiry_store', views.agency_inquiry_store, name='agency_inquiry_store'),  
    path('Add_adtype', views.Add_adtype, name='Add_adtype'),
    path('Add_adtype_store', views.Add_adtype_store, name='Add_adtype_store'),
    path('All_Adtype', views.All_Adtype, name='All_Adtype'),
    path('All_Adtype_delete/<int:id>', views.All_Adtype_delete, name='All_Adtype_delete'),
    path('All_Adtype_edit/<int:id>', views.All_Adtype_edit, name='All_Adtype_edit'),
    path('All_Adtype_update/<int:id>', views.All_Adtype_update, name='All_Adtype_update'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('edit_profile/<int:id>', views.edit_profile, name='edit_profile'),
    path('agency_update/<int:id>', views.agency_update, name='agency_update'),
    path('logout', views.logout, name='logout'),
    path('ChangePassword', views.ChangePassword, name='ChangePassword'),
    path('ChangePassword_chk', views.ChangePassword_chk, name='ChangePassword_chk'),
    path('order_front_page', views.order_front_page, name='order_front_page'),
    path('allOrder', views.allOrder, name='allOrder'),
    path('Approved_Order', views.Approved_Order, name='Approved_Order'),
    path('order_approve_process/<int:id>', views.order_approve_process, name = 'order_approve_process'),
    path('select-region/', views.SelectRegion, name='select_region'),
    path('get_cities_list/', views.get_cities_list, name = 'get_cities_list'),
    path('selected_region', views.selected_region, name='selected_region'),
    path('allRegion', views.allRegion, name='allRegion'),
    path('NewClassfiedTextOrder',views.NewClassfiedTextOrder, name="NewClassfiedTextOrder"),
    path('classfiedTextOrder',views.classfiedTextOrder, name="classfiedTextOrder"),
    path('approveOrder/<int:id>', views.approveOrder, name = 'approveOrder'),
    path('printedClassifiedTextOrder',views.printedClassifiedTextOrder, name="printedClassifiedTextOrder"),
    path('printOrder/<int:id>', views.printOrder, name = 'printOrder'),
    path('classifiedTextOrderViewmore/<int:id>', views.classifiedTextOrderViewmore, name = 'classifiedTextOrderViewmore'),
    path('NewClassifiedDisplayOrder', views.NewClassifiedDisplayOrder, name = 'NewClassifiedDisplayOrder'),
    path('classifiedDisplayOrder', views.classifiedDisplayOrder, name = 'classifiedDisplayOrder'),
    path('printedClassifiedDisplayOrder', views.printedClassifiedDisplayOrder, name = 'printedClassifiedDisplayOrder'),
    path('NewDisplayOrder', views.NewDisplayOrder, name = 'NewDisplayOrder'),
    path('DisplayOrder', views.DisplayOrder, name = 'DisplayOrder'),
    path('printedDisplayOrder', views.printedDisplayOrder, name = 'printedDisplayOrder'),
    path('allInquiry', views.allInquiry, name='allInquiry'),
    path('previewOrder/<int:id>', views.previewOrder, name='previewOrder'),
    
]