from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class VoteQuestion(models.Model):
    rate = models.IntegerField(default=0)

    question_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='question_votes')
    question_object_id = models.PositiveIntegerField()
    question_content_object = GenericForeignKey('question_content_type', 'question_object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return f"rate:{self.rate};\tquestion_content_type:{self.question_content_type};\tauthor:{self.author_id}"

    class Meta:
        unique_together = ('author', 'question_content_type', 'question_object_id',)


class VoteAnswer(models.Model):
    rate = models.IntegerField(default=0)

    answer_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='answer_votes')
    answer_object_id = models.PositiveIntegerField()
    answer_content_object = GenericForeignKey('answer_content_type', 'answer_object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return f"rate:{self.rate};\tanswer_content_type:{self.answer_content_type};\tauthor:{self.author_id}"

    class Meta:
        unique_together = ('author', 'answer_content_type', "answer_object_id",)


class TagManager(models.Manager):
    def sort_by_related_question_quantity(self):
        return self.annotate(num_questions=Count('question')).order_by('-num_questions')


class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TagManager()

    def __str__(self):
        return f"id: {self.id};\t title: {self.title}"


class QuestionManager(models.Manager):
    def sorted_by_rating(self):
        return self.annotate(total_question_votes=Sum('question_votes__rate')).order_by('-total_question_votes')

    def sorted_by_created_at(self):
        return self.order_by('-created_at')

    def filter_by_tag(self, tag_title):
        return self.filter(tags__title=tag_title)


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    votes = GenericRelation(VoteQuestion)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    objects = QuestionManager()

    def __str__(self):
        return f"title: {self.title};\t votes: {self.votes};"

    def get_rating(self):
        rating = self.votes.aggregate(Sum('rate'))['rate__sum']
        return rating if rating is not None else 0

    def answers_count(self):
        return Count(Answer.objects.filter(question_id=self.id))


class AnswerManager(models.Manager):
    def sorted_by_rating(self, question_id):
        return self.filter(question_id=question_id) \
            .annotate(total_answer_votes=Coalesce(Sum('answer_votes__rate'), 0)).order_by('-total_answer_votes')


class Answer(models.Model):
    body = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = GenericRelation(VoteAnswer)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    objects = AnswerManager()

    def __str__(self):
        return f"question_id: {self.question_id};\t votes: {self.votes}"

    def get_rating(self):
        rating = self.votes.aggregate(Sum('rate'))['rate__sum']
        return rating if rating is not None else 0


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    # author
