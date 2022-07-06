from django.urls  import path
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('verify/<str:token>/', verify, name='verify'),
    path('forget_password/', forget_password, name='forget_password'),
    path('change_password/<str:token>/', reset_password, name='reset_password'),
    path('login/', loginview, name='login'),
    path('logout/', logoutview, name='logout'),
]
