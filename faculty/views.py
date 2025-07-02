from django.shortcuts import render
from .models import Faculty

# Create your views here.

def faculty_list(request):
    faculty_list = Faculty.objects.all().order_by('-created_at')
    return render(request, 'faculty/faculty.html', {'faculty_list': faculty_list})
