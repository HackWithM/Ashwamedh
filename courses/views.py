from django.shortcuts import render, get_object_or_404
from .models import Course

# Create your views here.

def courses_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/courses.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})
