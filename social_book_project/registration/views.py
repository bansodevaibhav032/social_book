from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser 
from .filters import CustomUserFilter
from .forms import UploadFileForm, DisplayFileForm
from .models import UploadedFile
from rest_framework.views import APIView
from .serializers import UserSerializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
from datetime import datetime, timedelta
from jwt.exceptions import DecodeError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .decorators import has_uploaded_files
from .emails import *
from .serializers import VerifyAccountSerializers
from .emails import send_otp_via_mail
import random 

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = UserSerializers(data=data)
            if serializer.is_valid():
                user = serializer.save()

                # Generate OTP
                otp = generate_otp()

                # Send OTP via email
                send_otp_via_mail(user.email, otp)

                return Response({
                    'status': 200,
                    'message': 'Registration Successfully. Check Email!!',
                    'data': serializer.data,
                })
            return Response({
                'status': 400,
                'message': 'Something Went Wrong',
                'data': serializer.errors,
            })
        except Exception as e:
            print(e)

class Verify_OTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializers(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = CustomUser.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'Something Went Wrong',
                        'data': 'Invalid Email!!!',
                    })

                user = user.first()
                if user.otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Something Went Wrong',
                        'data': 'Wrong OTP',
                    })

                user.is_verified = True
                user.save()

                return Response({
                    'status': 200,
                    'message': 'Account Verified.',
                    'data': serializer.data,
                })

            return Response({
                'status': 400,
                'message': 'Something Went Wrong',
                'data': {},
            })

        except Exception as e:
            print(e)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=60),
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            
            response = Response({'token': token})
            response.set_cookie(key='jwt', value=token, httponly=True)

            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        except DecodeError:
            raise AuthenticationFailed('Invalid token')

        user = CustomUser.objects.get(id=payload['user_id'])
        serializer = UserSerializers(user)

        return Response(serializer.data)
class FileView(APIView):
    def get(self, request, title):
        file = get_object_or_404(UploadedFile, title=title)

        with open(file.file.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file.title}"'
            return response


@login_required(login_url='login')
def index(request):

    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        user = authenticate(request, email=email, password=pass1)

        if user is not None:
            user_obj = CustomUser.objects.get(email=email)

            if user_obj.is_verified:
                auth_login(request, user)
                return redirect('index')
            else:
                # Redirect to verification page if not verified
                return redirect('verify_otp_page', email=email)
        else:
            return HttpResponse('Email or password is incorrect!!!')

    return render(request, 'login.html')

def verify_otp_page(request, email):
    error_message = None

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        user_obj = CustomUser.objects.get(email=email)

        if user_obj.otp == entered_otp:
            # Correct OTP, mark user as verified and redirect to the index page
            user_obj.is_verified = True
            user_obj.save()
            return redirect('index')  # Redirect to your index page

        else:
            # Incorrect OTP, set an error message
            error_message = 'Incorrect OTP. Please try again.'

    return render(request, 'verify_otp_page.html', {'email': email, 'error_message': error_message})


def generate_otp():
    return str(random.randint(100000, 999999))

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        address = request.POST.get('address')
        public_visibility = request.POST.get('public_visibility') == 'on'
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        age = request.POST.get('age')
        birth_year = request.POST.get('birth_year')
        address = request.POST.get('address')

        if pass1 != pass2:
            return HttpResponse('Your Passwords are Not Matched')
        else:
            my_user = CustomUser.objects.create_user(email=email, password=pass1, age=age, birth_year=birth_year, address=address, public_visibility=public_visibility)
            
            otp = generate_otp()
            
            my_user.otp = otp
            my_user.save()

            send_otp_via_mail(email, otp)

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

@login_required(login_url='login')
def upload_books(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('uploaded_files')
    else:
        form = UploadFileForm()

    uploaded_files = UploadedFile.objects.filter(user=request.user)

    return render(request, 'uploadfile.html', {'form': form})

@login_required(login_url='login')
def uploaded_files(request):
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'uploadedfiles.html', {'uploaded_files': uploaded_files})


@login_required(login_url='login')
@has_uploaded_files
def uploaded_files(request):
    uploaded_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'uploadedfiles.html', {'uploaded_files': uploaded_files})
