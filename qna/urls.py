from django.urls import path 
from .views import *




urlpatterns = [
    path('', index, name='index'),
    path('add_poll/', add_poll, name='add_poll'),
    path('profile/', profile, name='profile'),
    path('edit_poll/<str:id>/', edit_poll, name='edit_poll'),
    path('edit_choice/<str:id>/', edit_choices, name='edit_choice'),
    path('poll/<str:id>/',poll_detail, name='poll_detail'),
    path('poll_vote/<str:id>/', poll_vote, name='poll_vote'),
    path('poll_result/<str:id>/', result_view, name='poll_result'),
]
