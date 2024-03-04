"""
URL configuration for social_book_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# social_book_project/urls.py
from django.contrib import admin
from django.urls import path,include
from registration import views
from django.conf import settings
from django.conf.urls.static import static
from registration.views import RegisterView,LoginView,UserView,Verify_OTP

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('index/', views.index, name='index'),
    path('logout/', views.logoutpage, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('faq/', views.faq, name='faq'),
    
    #leftsidebar
    path('form-basic/', views.form_basic, name='form_basic'),
    path('advanced-components/', views.advanced_components, name='advanced_components'),
    path('form-wizard/', views.form_wizard, name='form_wizard'),
    path('html5-editor/', views.html5_editor, name='html5_editor'),
    path('form-pickers/', views.form_pickers, name='form_pickers'),
    path('image-cropper/', views.image_cropper, name='image_cropper'),
    path('image-dropzone/', views.image_dropzone, name='image_dropzone'),   


    #Task
    path('authors-and-sellers/', views.authors_and_sellers, name='authors_and_sellers'),  
    path('upload_books/', views.upload_books, name='upload_books'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),

    #api
    path('api/', include('registration.urls')),

   
    
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)