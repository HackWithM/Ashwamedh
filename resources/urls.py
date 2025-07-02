from django.urls import path
from .views import book_list, question_paper_list, notes_list

urlpatterns = [
    path('resources/books/', book_list, name='books_list'),
    path('resources/question-papers/', question_paper_list, name='question_papers_list'),
    path('resources/notes/', notes_list, name='notes_list'),
] 