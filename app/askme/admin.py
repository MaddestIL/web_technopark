from django.contrib import admin
from .models import Question, Tag, QuestionLike, AnswerLike, Answer, Profile

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(AnswerLike)
admin.site.register(QuestionLike)
admin.site.register(Answer)
admin.site.register(Profile)
