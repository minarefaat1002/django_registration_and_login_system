from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return render(request,'users/home.html')
    
def register(request):
    if request.user.is_authenticated:
        return render(request,'users/profile.html')
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request,"email taken")
                return redirect('register')
            else:
                user =User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.success(request,"Your account has been created successfully. please try to login..")
                return redirect('login')
        else:
            messages.error(request,"password not matching...")
            return redirect('register')
    else:
        return render(request,'users/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('profile')
        else:
            messages.error(request,'invalid credentials')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            return render(request,'users/login.html')
@login_required
def profile(request):
    return render(request,'users/profile.html')