from django.shortcuts import render
from .models import Book, QuestionPaper, Note

# Create your views here.

def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'resources/book.html', {'books': books})

def question_paper_list(request):
    question_papers = QuestionPaper.objects.all().order_by('-created_at')
    return render(request, 'resources/question_paper.html', {'question_papers': question_papers})

def notes_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'resources/notes.html', {'notes': notes})
