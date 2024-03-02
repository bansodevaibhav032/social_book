from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser 
from .filters import CustomUserFilter
# from .models import UploadedFile
# from .forms import UploadFileForm
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

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
            # Include the 'algorithms' argument when decoding the JWT token
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
        # Perform any additional logic here if needed
        # For example, you might want to check user permissions or do some processing.
        # ...

        # Return the file content as a response
        with open(file.file.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file.title}"'
            return response


@login_required(login_url='login')
def index(request):

    return render(request, 'index.html')

def user_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        user=authenticate(request,email=email,password=pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('index')
        else:
            return HttpResponse('email or password is incorrect!!!')

    return render(request,'login.html')



def signup(request):
    if request.method == 'POST':
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
            my_user = CustomUser.objects.create_user(email=email, password=pass1, age=age, birth_year=birth_year, address=address,public_visibility=public_visibility)
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

@login_required(login_url='login')
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
