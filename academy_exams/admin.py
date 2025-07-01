from django.contrib import admin
from .models import Exam

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('is_active',)
