import random

import django
django.setup()
from django.core.management.base import BaseCommand
from mimesis import Person
from mimesis.locales import Locale
from askme.models import Question, Tag, VoteAnswer, VoteQuestion, Answer
from django.contrib.auth.models import User
from mimesis import Text
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Fill database with randomized content'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Indicates the number of rows to be created')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']


       # _fill_users(ratio)
        #_fill_tags(ratio)
        #_fill_questions(ratio * 10)
       # _fill_answers(ratio * 100)
        _fill_votes_answers(ratio * 250)
        _fill_votes_questions(ratio * 250)


def _fill_users(ratio):
    for i in range(ratio):
        person = Person(Locale.EN)

        try:
            u = User(first_name=person.first_name(),
                     last_name=person.last_name(),
                     email=person.email(),
                     password=person.password(),
                     is_staff=False,
                     username=person.username(),
                     )

            u.save()
        except IntegrityError:
            continue


def _fill_tags(ratio):
    for i in range(ratio):
        txt = Text(Locale.EN)
        try:
            t = Tag(title=txt.word())
            t.save()
        except IntegrityError:
            continue


def _fill_questions(ratio):
    for i in range(ratio):
        txt = Text(Locale.EN)
        random_user = User.objects.order_by('?').first()

        q = Question(title=txt.quote(),
                     body=txt.text(30),
                     author=random_user
                     )

        q.save()

        tags = Tag.objects.order_by('?')[:5]
        q.tags.set(tags)
        q.save()


def _fill_answers(ratio):
    for i in range(ratio):
        txt = Text(Locale.EN)
        random_user = None
        random_question = None

        while random_user is None:
            try:
                random_user = User.objects.get(pk=random.randint(1, 10000))
            except User.DoesNotExist:
                continue

        while random_question is None:
            try:
                random_question = Question.objects.get(pk=random.randint(1, 100000))
            except User.DoesNotExist:
                continue

        a = Answer(body=txt.text(30), author=random_user, question=random_question, is_correct=False)
        a.save()


def _fill_votes_questions(ratio):
    for i in range(ratio):
        question_model_instance = None
        while question_model_instance is None:
            try:
                question_model_instance = Answer.objects.get(pk=random.randint(1, 1_000_000))
            except Answer.DoesNotExist:
                continue
        votes = [-1, 1]

        random_user = None

        while random_user is None:
            try:
                random_user = User.objects.get(pk=random.randint(1, 10000))
            except User.DoesNotExist:
                continue

        vq = VoteQuestion(rate=random.sample(votes, 1)[0], author=random_user,
                          question_content_object=question_model_instance)
        vq.save()


def _fill_votes_answers(ratio):
    for i in range(ratio):
        answer_model_instance = None
        while answer_model_instance is None:
            try:
                answer_model_instance = Answer.objects.get(pk=random.randint(1, 1_000_000))
            except Answer.DoesNotExist:
                continue

        votes = [-1, 1]

        random_user = None

        while random_user is None:
            try:
                random_user = User.objects.get(pk=random.randint(1, 10000))
            except User.DoesNotExist:
                continue

        va = VoteAnswer(rate=random.sample(votes, 1)[0], author=random_user,
                        answer_content_object=answer_model_instance)
        va.save()
