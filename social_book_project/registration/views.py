from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('index')
        else:
            return HttpResponse('username or password is incorrect!!!')

    return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse('Your Password are Not Matched')
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login') 
    return render(request,'signup.html')


def logoutpage(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request, profile.html)

def faq(request):
    return render(request, faq.html)


#left side bar 

def form_basic(request):
    return render(request, 'form_basic.html')

def advanced_components(request):
    return render(request, 'advanced_components.html')

def form_wizard(request):
    return render(request, 'form_wizard.html')

def html5_editor(request):
    return render(request, 'html5_editor.html')

def form_pickers(request):
    return render(request, 'form_pickers.html')

def image_cropper(request):
    return render(request, 'image_cropper.html')

def image_dropzone(request):
    return render(request, 'image_dropzone.html')


