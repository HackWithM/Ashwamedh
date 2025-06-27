from django.shortcuts import render, get_object_or_404
from .models import Course, Resource, Faculty, ResourceCategory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

# Home page
def home(request):
    return render(request, 'academy/home.html')

# Courses listing
def courses(request):
    exam_type = request.GET.get('exam_type', '')
    q = request.GET.get('q', '')
    course_list = Course.objects.all()
    if exam_type:
        course_list = course_list.filter(exam_type=exam_type)
    if q:
        course_list = course_list.filter(title__icontains=q)
    paginator = Paginator(course_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'academy/courses.html', {'courses': page_obj.object_list, 'page_obj': page_obj})

# Course detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    recommended_resources = Resource.objects.filter(course=course)[:5]
    return render(request, 'academy/course_detail.html', {'course': course, 'recommended_resources': recommended_resources})

# Resources listing
def resources(request):
    exam_type = request.GET.get('exam_type', '')
    category = request.GET.get('category', '')
    year = request.GET.get('year', '')
    resource_list = Resource.objects.all()
    if exam_type:
        resource_list = resource_list.filter(course__exam_type=exam_type)
    if category:
        resource_list = resource_list.filter(category__name=category)
    if year:
        resource_list = resource_list.filter(created_at__year=year)
    paginator = Paginator(resource_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'academy/resources.html', {'resources': page_obj.object_list, 'page_obj': page_obj})

# Resource modal preview (HTMX)
def resource_modal(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    return render(request, 'academy/resource_modal.html', {'resource': resource})

# Dashboard
@login_required
def dashboard(request):
    student = getattr(request.user, 'student', None)
    enrolled_courses = student.enrolled_courses.all() if student else []
    recommended_resources = Resource.objects.all()[:5]
    announcements = []  # Placeholder
    return render(request, 'academy/dashboard.html', {
        'enrolled_courses': enrolled_courses,
        'recommended_resources': recommended_resources,
        'announcements': announcements,
    })

# About
def about(request):
    return render(request, 'academy/about.html')

# Faculty
def faculty(request):
    faculty_list = Faculty.objects.all()
    return render(request, 'academy/faculty.html', {'faculty_list': faculty_list})

# Contact
@csrf_protect
def contact(request):
    success = False
    if request.method == 'POST':
        # Here you would send email using Django's EmailBackend
        success = True
    return render(request, 'academy/contact.html', {'success': success})

# Auth pages (use Django's built-in views in real app, but placeholder here)
def login_view(request):
    return render(request, 'academy/registration/login.html', {'form': {}})

def signup_view(request):
    return render(request, 'academy/registration/signup.html', {'form': {}})

def password_reset_view(request):
    return render(request, 'academy/registration/password_reset.html', {'form': {}})

def password_reset_done_view(request):
    return render(request, 'academy/registration/password_reset_done.html')
