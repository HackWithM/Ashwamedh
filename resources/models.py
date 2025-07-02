from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/books/')
    image = models.ImageField(upload_to='resources/book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QuestionPaper(models.Model):
    EXAM_CHOICES = [
        ('MPSC', 'MPSC'),
        ('UPSC', 'UPSC'),
        # Add more as needed
    ]
    sr_no = models.PositiveIntegerField(blank=True, null=True)
    advt_no = models.CharField(max_length=20, blank=True, null=True)
    exam_type = models.CharField(max_length=10, choices=EXAM_CHOICES, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_of_publication = models.DateField(blank=True, null=True)
    file = models.FileField(upload_to='resources/question_papers/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/notes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
