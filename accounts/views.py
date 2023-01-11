from django.shortcuts import render,redirect
from .forms import UserForm
from django.http import HttpResponse
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from .utils import role_check,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Create your views here.

#function to allow only vendor to access the vendDsahboard page 
def role_check_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
def role_check_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def registerUser(requests):
    if requests.user.is_authenticated :
        messages.info(requests,'Your are already logged in')
        return redirect('dashboard')
    elif requests.method == "POST":
        print(requests.POST)
        form = UserForm(requests.POST)
        # if form.is_valid():
        #     password = form.cleaned_data['password']
        #     user =form.save(commit=False)
        #     user.set_password(password)
        #     user.role = User.CUSTOMER
        #     user.save()
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()
            #send verification email 
            send_verification_email(requests,user,'registerUser')
            messages.success(requests,'Account got registered successfully')
            return redirect('registerUser')
        else:
            print(form.errors)
            messages.error(requests,form.errors.items)
            return redirect('registerUser')
        #return render(requests,'accounts/errorlist.html',{'form':form})
        
 
    else:
        context ={
            'form':UserForm()
        }
        return render(requests,'accounts/registerUser.html',context)

def registerVendor(request):
    if request.user.is_authenticated :
        messages.info(request,'Your are already logged in')
        return redirect('dashboard')
    elif request.method =='POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.RESTAURANT
            user.save()
            vendor =v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
            send_verification_email(request,user,'registerVendor')
            messages.success(request,"Registration from submitted successfully")
            return redirect('registerVendor')
        else:
            print(form.errors.values())
            for error in form.errors.values():
                messages.error(request,error)
            
            print(v_form.errors.values())
            for error in v_form.errors.values():
                messages.error(request,error)
            return redirect('registerVendor')
    else:
        form = UserForm()
        v_form = VendorForm()
        context = {
            'form':form,
            'v_form':v_form
        }
        return render(request,'accounts/registerVendor.html',context)

def login(request):
    if request.user.is_authenticated :
        messages.info(request,'Your are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Your are not logged in !!')
            return redirect('myAccount')
        else:
            messages.error(request,'Invalid login credentials !!')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.user.is_authenticated:    
        auth.logout(request)
        messages.info(request,'User is Logged Out !!!')
        return redirect('login')
    else:
        messages.info(request,'Customer needs to loggedin before logout')
        return redirect('login')

def dashboard(request):
    return render(request,'accounts/dashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    print(user.role)
    redirectlink = role_check(user)
    print('Redirection url :',redirectlink)
    return redirect(redirectlink)

@login_required(login_url='login')
@user_passes_test(role_check_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(role_check_vendor)
def vendDashboard(request):
    return render(request,'accounts/vendDashboard.html')


def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,OverflowError,ValueError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'Activation successful')
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid Activation link')
        return redirect('registerUser')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        if User.objects.filter( email=email).exists():
            user = User.objects.get(email__iexact = email)
            send_verification_email(request,user,'forgot_password')
            messages.info(request,"Verification mail has been sent")
            return redirect('forgot_password')
        else:
            messages.error(request,'Email id provided doesnot exist')
            return redirect('forgot_password')

    else:
        return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,OverflowError,ValueError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Email verification successful')
        return redirect('reset_password')
    else:
        messages.error(request,'Invalid Activation link')
        return redirect('forgot_password')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        uid = request.session['uid']
        user = User.objects.get(pk=uid)
        if password == confirm_password:
            user.set_password(password)
            user.is_active =True
            user.save()
            messages.success(request,"Password Successfully Updated !!!")
            return redirect('login')
        else:
            return redirect('reset_password')
    else:
        return render(request,'accounts/reset_password.html')