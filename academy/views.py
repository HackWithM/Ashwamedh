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
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import StudentRegistrationForm
from .models import StudentProfile
from django.views.decorators.csrf import csrf_exempt

import json

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

def popup_contact_view(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if 'otp' in request.POST:
                # OTP verification step
                if request.POST['otp'] == request.session.get('popup_otp'):
                    # Send email to admin
                    send_mail(
                        'New Enquiry from ' + request.session['popup_username'],
                        f"Name: {request.session['popup_username']}\nEmail: {request.session['popup_email']}\nMobile: {request.session['popup_mobile_no']}\nMessage: {request.session['popup_message']}",
                        settings.EMAIL_HOST_USER,
                        [settings.ADMIN_EMAIL]
                    )
                    send_fast2sms_admin(
                        settings.ADMIN_MOBILE,
                        f"New enquiry from {request.session['popup_username']} ({request.session['popup_mobile_no']}): {request.session['popup_message']}"
                    )
                    # Clear session
                    for key in ['popup_otp', 'popup_username', 'popup_email', 'popup_mobile_no', 'popup_message']:
                        if key in request.session:
                            del request.session[key]
                    return JsonResponse({'success': True, 'message': 'Thank you! Your enquiry has been submitted.'})
                else:
                    return JsonResponse({'success': False, 'otp_error': True, 'message': 'Invalid OTP. Please try again.'})
            else:
                # First form submission
                form = ContactForm(request.POST)
                if form.is_valid():
                    otp = str(random.randint(1000, 9999))
                    request.session['popup_otp'] = otp
                    request.session['popup_username'] = form.cleaned_data['username']
                    request.session['popup_email'] = form.cleaned_data['email']
                    request.session['popup_mobile_no'] = form.cleaned_data['mobile_no']
                    request.session['popup_message'] = form.cleaned_data['message']
                    send_mail(
                        'Your OTP for Ashwamedh Academy',
                        f'Your OTP is: {otp}',
                        settings.EMAIL_HOST_USER,
                        [form.cleaned_data['email']]
                    )
                    return JsonResponse({'otp_sent': True, 'mobile_no': form.cleaned_data['mobile_no']})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors, 'message': 'Please correct the errors below.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request.'})
    else:
        return render(request, 'academy/popup_contact_form.html')

def send_registration_otp(email, otp):
    send_mail(
        'Your Registration OTP for Ashwamedh Academy',
        f'Your OTP is: {otp}',
        settings.EMAIL_HOST_USER,
        [email]
    )

@csrf_exempt
def ajax_register_student(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = request.POST
        if 'otp' in data:
            # OTP verification step
            if data['otp'] == request.session.get('reg_otp'):
                # Create user and profile
                user = User.objects.create_user(
                    username=request.session['reg_email'],
                    email=request.session['reg_email'],
                    password=request.session['reg_password'],
                    first_name=request.session['reg_first_name'],
                    last_name=request.session['reg_last_name']
                )
                profile = user.studentprofile
                profile.address = request.session['reg_address']
                profile.mobile = request.session['reg_mobile']
                # Handle profile_pic if uploaded
                if 'reg_profile_pic' in request.session:
                    profile.profile_pic = request.session['reg_profile_pic']
                profile.save()
                login(request, user)
                # Clear session
                for key in ['reg_otp','reg_first_name','reg_last_name','reg_email','reg_password','reg_address','reg_mobile','reg_profile_pic']:
                    if key in request.session:
                        del request.session[key]
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP'})
        else:
            # First form submission
            form = StudentRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                otp = str(random.randint(1000, 9999))
                request.session['reg_otp'] = otp
                request.session['reg_first_name'] = form.cleaned_data['first_name']
                request.session['reg_last_name'] = form.cleaned_data['last_name']
                request.session['reg_email'] = form.cleaned_data['email']
                request.session['reg_password'] = form.cleaned_data['password']
                request.session['reg_address'] = form.cleaned_data['address']
                request.session['reg_mobile'] = form.cleaned_data['mobile']
                if 'profile_pic' in request.FILES:
                    request.session['reg_profile_pic'] = request.FILES['profile_pic'].name
                send_registration_otp(form.cleaned_data['email'], otp)
                return JsonResponse({'otp_sent': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def profile_view(request):
    profile = request.user.studentprofile
    return render(request, 'academy/profile.html', {'profile': profile})
