from django.urls import path
from .views import faculty_list

urlpatterns = [
    path('faculty/', faculty_list, name='faculty_list'),
] 