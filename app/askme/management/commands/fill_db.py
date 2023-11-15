
import django
django.setup()

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from askme.models import Question, Answer, AnswerLike, QuestionLike, Tag, Profile
from django.utils.crypto import get_random_string
from faker import Faker
import random

Fake = Faker()


class Command(BaseCommand):
    help = 'Fiil database with fake data'
    images = ['img/avatar-1.png', 'img/avatar-2.jpeg', 'img/avatar-3.jpeg']

    def handle(self, *args, **options):
        ratio = options['ratio']


    def fill_users(ratio):
        users = []
        for _ in range(ratio):
            user = User(first_name=Fake.name(), email=Fake.email(), password=Fake.password())
            users.append(user)
        User.objects.bulk_create(users, ignore_conflicts=True)

        saved_users = User.objects.all()
        profiles = []
        for user in saved_users:
            profiles.append(Profile(user=user))
        Profile.objects.bulk_create(profiles, ignore_conflicts=True)

    def fill_tags(ratio):
        tags=[]
        for i in range(ratio):
            words = list(set([get_random_string(int((random.random() * 100)) % 6 + 1) for _ in range(ratio * 2)]))[
                    :ratio]
            tag = [Tag(title=word) for word in words]
            tags.append(tag)
        Tag.objects.bulk_create(tags, ignore_conflicts=True)
    def fill_question(ratio):

        profiles = list(Profile.objects.all())
        random.shuffle(Profile)
        questions = []
        time = Fake.date_between()
        for i in range(ratio * 10):

            question = Question(
                author=profiles[i % (len(profiles) or 1)],
                title=Fake.text(max_nb_chars=int((random.random() * 10000)) % 20 + 10),
                description=Fake.text(max_nb_chars=int((random.random() * 10000)) % 700 + 30),
                creating_time=Fake.date_time_between(time)
            )
            questions.append(question)
        Question.objects.bulk_create(questions, ignore_conflicts=True)

        questions_likes = []
        saved_question = Question.objects.all()
        for question in saved_question:
            questions_like = QuestionLike(
                question=question,
                type=1 if int((random.random() * 100)) % 2 == 0 else -1,
                author=profiles[int((random.random() * 10000)) % ratio]
            )
            questions_likes.append(questions_like)
        Question.objects.bulk_create(questions_likes, ignore_conflicts=True)

    def fill_answer(ratio):
        answers = []
        profiles = list(Profile.objects.all())
        random.shuffle(profiles)
        questions = list(Question.objects.all())
        for i in range(ratio):
            time = Fake.date_between()
            answer = Answer(
                author=profiles[i % (len(profiles) or 1)],
                description=Fake.text(max_nb_chars=int((random.random() * 10000)) % 300 + 30),
                creating_time=Fake.date_time_between(time),
                question=questions[i % (len(profiles) or 1)]
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers, ignore_conflicts=True)

        saved_answer = list(Answer.objects.all())
        answers_likes = []
        for answer in saved_answer:
            answers_like = AnswerLike(
                answer=answer,
                type=1 if int((random.random() * 100)) % 2 == 0 else -1,
                author=profiles[int((random.random() * 10000)) % ratio]
            )
            answers_likes.append(answers_like)
        AnswerLike.objects.bulk_create(answers_likes)





    def add_arguments(self, parser):
        parser.add_argument(
            'ratio',
            type=int,
            default=0,
            help='Коэфициент заполнения сущностей'
        )