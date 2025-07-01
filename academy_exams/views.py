from django.shortcuts import render
from .models import Exam

# Create your views here.

def exams_list(request):
    exams = Exam.objects.filter(is_active=True)
    return render(request, 'academy_exams/exams.html', {'exams': exams})
