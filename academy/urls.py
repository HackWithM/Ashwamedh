from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

urlpatterns = [
    path('', views.home, name='home'),
    # path('courses/', views.courses, name='courses'),  # Removed: handled by courses app now
    # path('courses/<int:course_id>/', views.course_detail, name='course_detail'),  # Removed: handled by courses app now
    path('resources/', views.resources, name='resources'),
    path('resources/<int:resource_id>/modal/', views.resource_modal, name='resource_modal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('exams/<str:exam_slug>/', views.exam_detail, name='exam_detail'),
    path('academy/<str:exam>.html', lambda request, exam: redirect(f'/exams/{exam}/', permanent=True)),
    path('popup-contact/', views.popup_contact_view, name='popup_contact'),
] 