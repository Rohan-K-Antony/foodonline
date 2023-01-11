from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def role_check(user):
    redirectlink = ''
    if user.role == 2:
        redirectlink ='custDashboard'
    elif user.role == 1:
        redirectlink = 'venDashboard'
    elif user.role is None and user.is_superadmin is True:
        redirectlink = '/admin'
    return redirectlink

def send_verification_email(request,user,from_view):
    current_site = get_current_site(request)
    mail_subject = "Please activate you account"
    message=''
    if from_view is 'registerUser' and from_view is 'registerVendor':
        message = render_to_string('accounts/emails/account_verification_email.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
        })
    elif from_view is 'forgot_password':
        message = render_to_string('accounts/emails/account_verification_email_forgot_password.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user)
        })
    to_email = user.email
    mail = EmailMessage(mail_subject,message,to=[to_email])
    mail.send()