import random
from django.shortcuts import render
from .models import Question, Category

def home(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        questions = Question.objects.filter(category_id=selected_category)
    else:
        questions = Question.objects.all()

    if questions:
        question = random.choice(questions)
    else:
        question = None

    return render(request, 'home.html', {
        'question': question,
        'categories': categories,
        'selected_category': selected_category
    })