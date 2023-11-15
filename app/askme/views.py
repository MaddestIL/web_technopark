from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Question, Answer


def paginate(request, obj_list, num_per_page=5):
    paginator = Paginator(obj_list, num_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    return objects


def index(request):
    questions = Question.objects.sorted_by_created_at()
    return render(request, 'index.html', {'questions': paginate(request, questions)})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question doesn't exist!")

    answers = Answer.objects.get_answers_for_question(question_id)

    return render(request, 'question.html', {'question': question, 'answers': paginate(request, answers)})


def tag(request, slug):
    questions = Question.objects.filter_by_tag(slug)
    return render(request, 'tag.html', {'tag': slug, 'questions': paginate(request, questions)})


def hot(request):
    questions = Question.objects.get_hot_questions()

    return render(request, 'index.html', {'questions': paginate(request, questions)})
