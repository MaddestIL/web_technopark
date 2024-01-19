from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib.auth.models import User

from .models import Question, QuestionLike, AnswerLike, Answer, Tag, Profile





@require_http_methods(['GET'])
def index(request):
    page_obj = paginate(Question.objects.get_all(), request)
    context = {
        'page_obj': page_obj,
        'global_tags': Tag.objects.get_popular()[:10],
               }
    return render(request, 'index.html', context=context)


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
def settings(request, user_id):
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





@require_http_methods(['GET', 'POST'])
def question(request, question_id: int):
    page_obj = paginate(Answer.objects.filter(question_id=question_id), request, 3)
    context = {'question': Question.objects.get(pk=question_id),
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               'page_obj': page_obj,
               }
    return render(request, 'question.html', context=context)

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)

