from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    EXAM_TYPE_CHOICES = [
        ("IAS", "IAS"),
        ("IPS", "IPS"),
        ("UPSC", "UPSC"),
        ("MPSC", "MPSC"),
    ]
    title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    short_description = models.CharField(max_length=300)
    detailed_syllabus = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    thumbnail = models.ImageField(upload_to="course_thumbnails/")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class ResourceCategory(models.Model):
    CATEGORY_CHOICES = [
        ("Book", "Book"),
        ("Question Paper", "Question Paper"),
        ("Note", "Note"),
        ("Syllabus", "Syllabus"),
        ("VideoLecture", "Video Lecture"),
    ]
    name = models.CharField(max_length=30, choices=CATEGORY_CHOICES, unique=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Resource Categories"

    def __str__(self):
        return self.name

class Resource(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.CharField(max_length=100)
    pdf_or_file_upload = models.FileField(upload_to="resources/")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to="faculty_photos/")

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    enrolled_courses = models.ManyToManyField(Course, related_name="enrolled_students", blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='student_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    profile = getattr(instance, 'studentprofile', None)
    if profile:
        profile.save()
