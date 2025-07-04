from django.shortcuts import render, get_object_or_404
from .models import Course, Resource, Faculty, ResourceCategory
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import Http404
import random
import requests
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm

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

def exam_detail(request, exam_slug):
    template_name = f'academy/{exam_slug}.html'
    try:
        return render(request, template_name)
    except Exception:
        raise Http404("Exam page not found.")

def send_fast2sms_otp(mobile, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "route": "q",
        "message": f"Your OTP for Ashwamedh Academy is {otp}",
        "language": "english",
        "flash": 0,
        "numbers": mobile
    }
    headers = {
        'authorization': settings.FAST2SMS_API_KEY,
        'Content-Type': "application/x-www-form-urlencoded"
    }
    requests.post(url, data=payload, headers=headers)

def send_fast2sms_admin(mobile, msg):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "route": "q",
        "message": msg,
        "language": "english",
        "flash": 0,
        "numbers": mobile
    }
    headers = {
        'authorization': settings.FAST2SMS_API_KEY,
        'Content-Type': "application/x-www-form-urlencoded"
    }
    requests.post(url, data=payload, headers=headers)

def contact_view(request):
    if request.method == 'POST':
        if 'otp' in request.POST:
            # OTP verification step
            if request.POST['otp'] == request.session.get('otp'):
                # Send email to admin
                send_mail(
                    'New Enquiry from ' + request.session['username'],
                    f"Name: {request.session['username']}\nEmail: {request.session['email']}\nMobile: {request.session['mobile_no']}\nMessage: {request.session['message']}",
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL]
                )
                # Send SMS to admin
                send_fast2sms_admin(
                    settings.ADMIN_MOBILE,
                    f"New enquiry from {request.session['username']} ({request.session['mobile_no']}): {request.session['message']}"
                )
                # Clear session
                for key in ['otp', 'username', 'email', 'mobile_no', 'message']:
                    if key in request.session:
                        del request.session[key]
                return render(request, 'academy/contact.html', {'success': True})
            else:
                return render(request, 'academy/contact.html', {'otp_error': True, 'otp_sent': True})
        else:
            # First form submission
            form = ContactForm(request.POST)
            if form.is_valid():
                otp = str(random.randint(1000, 9999))
                request.session['otp'] = otp
                request.session['username'] = form.cleaned_data['username']
                request.session['email'] = form.cleaned_data['email']
                request.session['mobile_no'] = form.cleaned_data['mobile_no']
                request.session['message'] = form.cleaned_data['message']
                # Send OTP to user's email instead of SMS
                send_mail(
                    'Your OTP for Ashwamedh Academy',
                    f'Your OTP is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']]
                )
                return render(request, 'academy/contact.html', {'otp_sent': True, 'mobile_no': form.cleaned_data['mobile_no']})
    else:
        form = ContactForm()
    return render(request, 'academy/contact.html', {'form': form})
