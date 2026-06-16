from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'save/<int:question_id>/',
        views.save_question,
        name='save_question'
    ),

    path(
        'my-questions/',
        views.my_questions,
        name='my_questions'
    ),

    path(
        'delete-saved/<int:saved_id>/',
        views.delete_saved_question,
        name='delete_saved_question'
    ),

    path(
        'ai-generate/',
        views.ai_generate_question,
        name='ai_generate_question'
    ),

    path(
        'api/random-question/',
        views.random_question,
        name='random_question'
    ),

    path(
        'api/ai-generate/',
        views.ai_generate_question_api,
        name='ai_generate_question_api'
    ),
]