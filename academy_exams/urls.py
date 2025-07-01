from django.urls import path
from .views import exams_list

urlpatterns = [
    path('exams/', exams_list, name='exams_list'),
] 