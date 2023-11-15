from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib.auth.models import User

from .models import Question, QuestionLike, AnswerLike, Answer, Tag, Profile


def paginate(request, data, count=10):
    paginator = Paginator(data, count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    last_page = len(paginator.page_range)
    return page_obj, last_page


@require_http_methods(['GET'])
def index(request):
    questions = Question.objects.get_all_ids()
    page_obj, last_page = paginate(request, questions, 10)
    data = Question.objects.get_all(page_obj)
    context = {
        'last_page': last_page,
        'page_obj': page_obj,
        'data': data,
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best()
    }
    return render(request, 'all_questions.html', context=context)


@require_http_methods(['GET'])
def tag_questions(request, tag):
    questions = Question.objects.get_by_tag_ids(tag)
    page_obj, last_page = paginate(request, questions, 10)
    data = Question.objects.get_all(page_obj)
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'data': data,
        'last_page': last_page,
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best()
    }
    return render(request, 'tag_questions.html', context=context)


@require_http_methods(['GET'])
def hot_questions(request):
    questions = Question.objects.get_hot_ids(30)
    page_obj, last_page = paginate(request, questions, 10)
    data = Question.objects.get_all(page_obj)
    context = {
        'page_obj': page_obj,
        'data': data,
        'last_page': last_page,
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best()
    }
    return render(request, 'hot_questions.html', context=context)


@require_http_methods(['GET'])
def best_questions(request):
    questions = Question.objects.get_best_ids(30)
    page_obj, last_page = paginate(request, questions, 10)
    data = Question.objects.get_all(page_obj)
    context = {
        'page_obj': page_obj,
        'data': data,
        'last_page': last_page,
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best()
    }
    return render(request, 'best_questions.html', context=context)


@require_http_methods(['GET'])
def new_questions(request):
    questions = Question.objects.get_new_ids()
    page_obj, last_page = paginate(request, questions, 10)
    data = Question.objects.get_all(page_obj)
    context = {
        'page_obj': page_obj,
        'data': data,
        'last_page': last_page,
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best()
    }
    return render(request, 'new_questions.html', context=context)


@require_http_methods(['GET', 'POST'])
def signup(request):
    context = {
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best(),
    }
    return render(request, 'signup.html', context=context)


@require_http_methods(['GET', 'POST'])
def signin(request):
    cont = request.GET.get('continue')

    context = {
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best(),
        'continue': cont
    }
    return render(request, 'signin.html', context=context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def settings(request):
    user = get_object_or_404(User, id=request.user.id)
    user_id = user.id
    context = {
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best(),
    }
    return render(request, 'settings.html', context=context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def ask(request):
    context = {
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best(),
    }
    return render(request, 'ask.html', context=context)


def custom_paginate(obj, data, count=10):
    page = obj // count + 1
    paginator = Paginator(data, count)
    page_obj = paginator.get_page(page)
    last_page = len(paginator.page_range)
    return page_obj, last_page


@require_http_methods(['GET', 'POST'])
def question(request, question_id: int):
    question_item = get_object_or_404(Question, pk=question_id)
    is_author = False
    if question_item.author.user == request.user:
        is_author = True
    context = {
        'question': Question.objects.get_obj(question_item),
        'ptags': Tag.objects.get_popular(),
        'bmembers': Profile.objects.get_best(),
        'author': is_author
    }
    return render(request, 'question.html', context=context)



