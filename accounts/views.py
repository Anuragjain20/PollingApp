from django.shortcuts import render,redirect,HttpResponse
from .forms import *
import uuid
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages 
# Create your views here.


def register(request):
    try:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User registration successful. Please verify your email address to login.')
                return redirect('/accounts/login')
        else:
            form = UserForm()
        return render(request, 'register.html', {'form': form})
    except Exception as e:
        print(e)
        form = UserForm()
        messages.error(request,"Something went wrong with your registration. Please try again")
        
        return render(request, 'register.html', {'form': form})

def verify(request,token):
    try:
        user = User.objects.get(email_verification_token=token)
        user.is_verified = True
     
        user.save()
        messages.success(request,"Email Verified Successfully")
       
        return redirect('/accounts/login/')
    except Exception as e:
        print(e)
        messages.error(request,"Something went wrong with your verification. Please try again") 


def forget_password(request):
    try:
        if request.method == 'POST':
            form = ForgetPasswordForm(request.POST)
            if form.is_valid():
                token = str(uuid.uuid4())
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)
                forget_password_obj = ForgetPassword.objects.create(user=user,forget_password_token=token)

                return HttpResponse('<h1>Password Reset Link Sent</h1>')
        else:
            form = ForgetPasswordForm()
        return render(request, 'forget_password.html', {'form': form})
    except Exception as e:
        print(e)
        form = ForgetPasswordForm()
        messages.error(request,"Something went wrong with your password reset. Please try again")
        return render(request, 'forget_password.html', {'form': form})             


def reset_password(request,token):
    try:
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password1']
                print(password)
                user = ForgetPassword.objects.get(forget_password_token=token).user
                user.set_password(password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return redirect('/accounts/login/')
            else:
                messages.error(request, 'Something went wrong with your password reset. Please try again')
                
                return redirect('/accounts/change_password/'+token)    
          
        else:
            form = ResetPasswordForm()
        return render(request, 'reset_password.html', {'form': form})
    except Exception as e:
        print(e)
        form = ForgetPasswordForm()
        messages.error(request,"Something went wrong with your password reset. Please try again")
        return render(request, 'reset_password.html', {'form': form})

def loginview(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(email=email,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('/')
                else:
                    messages.error(request, 'Invalid email or password')
                    return redirect('/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    except Exception as e:
        print(e)
        form = LoginForm()
        messages.error(request,"Something went wrong with your login. Please try again")
        return render(request, 'login.html', {'form': form})

def logoutview(request):
    try:
        logout(request)
        return redirect('/accounts/login/')
    except Exception as e:
        print(e)
        messages.error(request,"Something went wrong with your logout. Please try again")
        return redirect('/')