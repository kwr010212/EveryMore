import random

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import os
from openai import OpenAI

from .models import (
    Question,
    Category,
    SavedQuestion
)

from django.http import JsonResponse


def random_question(request):

    category_id = request.GET.get("category")

    questions = Question.objects.all()

    if category_id:
        questions = questions.filter(
            category_id=category_id
        )

    question = random.choice(list(questions))

    return JsonResponse({
        "id": question.id,
        "text": question.text,
        "category": question.category.name,
        "is_ai": question.is_ai_generated
    })


def home(request):
    categories = Category.objects.all()

    selected_category = request.GET.get('category')

    if selected_category in [None, "", "None"]:
        selected_category = None
    search = request.GET.get('search')

    questions = Question.objects.all()

    if selected_category:
        questions = questions.filter(
            category_id=selected_category
        )

    if search:
        questions = questions.filter(
            text__icontains=search
        )

    question_id = request.GET.get('question_id')

    if question_id:

        try:
            question = Question.objects.get(
                id=question_id
            )

        except Question.DoesNotExist:
            question = None

    else:

        if questions:
            question = random.choice(questions)
        else:
            question = None

    return render(
        request,
        'home.html',
        {
            'question': question,
            'categories': categories,
            'selected_category': selected_category,
            'search': search
        }
    )


@login_required
def save_question(request, question_id):

    question = Question.objects.get(
        id=question_id
    )

    SavedQuestion.objects.get_or_create(
        user=request.user,
        question=question
    )

    return redirect(
        f"/everymore/?question_id={question.id}"
    )

@login_required
def my_questions(request):

    saved_questions = SavedQuestion.objects.filter(
        user=request.user
    ).order_by('-saved_at')

    return render(
        request,
        'my_questions.html',
        {
            'saved_questions': saved_questions
        }
    )

@login_required
def delete_saved_question(request, saved_id):

    saved_question = SavedQuestion.objects.get(
        id=saved_id,
        user=request.user
    )

    saved_question.delete()

    return redirect('my_questions')

@login_required
def ai_generate_question(request):

    category_id = request.GET.get('category')

    print("category_id =", category_id)

    api_key = os.getenv("OPENAI_API_KEY")


    client = OpenAI(
        api_key=api_key
    )

    if category_id and category_id != "None":

        category = Category.objects.get(
            id=category_id
        )

        prompt = f"""
        '{category.name}' 카테고리에 맞는
        자기성찰 질문 1개를 생성해줘.

        조건:
        - 한국어
        - 질문만 출력
        - 50자 이하
        """

    else:

        category = random.choice(
            Category.objects.all()
        )

        prompt = """
        신앙, 관계, 비전, 일상 중 하나를 주제로

        자기성찰 질문 1개를 생성해줘.

        조건:
        - 한국어
        - 질문만 출력
        - 50자 이하
        """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    ai_question = response.output_text.strip()

    existing_question = Question.objects.filter(
        text=ai_question
    ).first()

    if existing_question:

        question = existing_question

    else:

        question = Question.objects.create(
            text=ai_question,
            category=category,
            is_ai_generated=True
        )

    return redirect(
        f"/everymore/?question_id={question.id}"
    )

@login_required
def ai_generate_question_api(request):

    category_id = request.GET.get('category')

    print("category_id =", category_id)

    api_key = os.getenv("OPENAI_API_KEY")



    client = OpenAI(
        api_key=api_key
    )

    if category_id and category_id != "None":

        category = Category.objects.get(
            id=category_id
        )

        prompt = f"""
        '{category.name}' 카테고리에 맞는
        자기성찰 질문 1개를 생성해줘.

        조건:
        - 한국어
        - 질문만 출력
        - 50자 이하
        """

    else:

        category = random.choice(
            Category.objects.all()
        )

        prompt = """
        신앙, 관계, 비전, 일상 중 하나를 주제로

        자기성찰 질문 1개를 생성해줘.

        조건:
        - 한국어
        - 질문만 출력
        - 50자 이하
        """

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

    except Exception as e:

        print("OPENAI ERROR:", str(e))

        return JsonResponse({
            "error": str(e)
        }, status=500)

    ai_question = response.output_text.strip()

    existing_question = Question.objects.filter(
        text=ai_question
    ).first()

    if existing_question:

        question = existing_question

    else:

        question = Question.objects.create(
            text=ai_question,
            category=category,
            is_ai_generated=True
        )

    return JsonResponse({

        "id": question.id,

        "text": question.text,

        "category": question.category.name,

        "is_ai": question.is_ai_generated

    })