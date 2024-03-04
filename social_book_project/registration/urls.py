from django.urls import path
from .views import RegisterView,LoginView,UserView,FileView,Verify_OTP

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('verifyotp/',Verify_OTP.as_view()),
    path('login/',LoginView.as_view()),
    path('user/',UserView.as_view()),
    path('files/<str:title>/', FileView.as_view(), name='file-view-by-title'),
]

