from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser 
from .filters import CustomUserFilter
from .models import UploadedFile
from .forms import UploadFileForm


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
            return HttpResponse('email or password is incorrect!!!')

    return render(request,'login.html')



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        address= request.POST.get('address')
        public_visibility = request.POST.get('public_visibility') == 'on'
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        age = request.POST.get('age')
        birth_year = request.POST.get('birth_year')
        address = request.POST.get('address')

        if pass1 != pass2:
            return HttpResponse('Your Passwords are Not Matched')
        else:
            my_user = CustomUser.objects.create_user(email=email, username=username, password=pass1, age=age, birth_year=birth_year, address=address,public_visibility=public_visibility)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')


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


def authors_and_sellers(request):
    user_filter = CustomUserFilter(request.GET, queryset=CustomUser.objects.all())
    users = user_filter.qs

    context = {
        'users': users,
        'user_filter': user_filter,
    }

    return render(request, 'authors_and_sellers.html', context)


@login_required
def upload_books(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('upload_books')
    else:
        form = UploadFileForm()

    uploaded_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'uploadfile.html', {'form': form, 'uploaded_files': uploaded_files})