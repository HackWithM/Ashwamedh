from django.shortcuts import render
from .models import Book, QuestionPaper, Note

# Create your views here.

def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'resources/book.html', {'books': books})

def question_paper_list(request):
    qs = QuestionPaper.objects.all()
    title = request.GET.get('title')
    if title:
        qs = qs.filter(title__icontains=title)
    return render(request, 'resources/question_paper.html', {'question_papers': qs})

def notes_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'resources/notes.html', {'notes': notes})
