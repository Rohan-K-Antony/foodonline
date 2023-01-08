from django.shortcuts import render,redirect
from .forms import UserForm
from django.http import HttpResponse
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
# Create your views here.
def registerUser(requests):

    if requests.method == "POST":
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

    if request.method =='POST':
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