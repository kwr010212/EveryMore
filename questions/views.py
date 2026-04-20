from django.shortcuts import render
from .models import Question

def home(request):
    questions = Question.objects.all()
    return render(request, 'home.html', {'questions': questions})