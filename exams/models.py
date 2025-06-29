from django.db import models

class Exam(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='exam_logos/')
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
