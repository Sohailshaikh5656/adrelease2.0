
from django.core.mail import send_mail
import uuid
from django.conf import settings


def send_forget_password_mail(email,password,username):

	
	subject = 'You Forget Password'
	message = f'Hi Admin, {username},\n Your password is {password}, \n Thanks and regardss'
	email_form = settings.EMAIL_HOST_USER
	recipient_list = [email]
	send_mail(subject, message, email_form, recipient_list)
	return True