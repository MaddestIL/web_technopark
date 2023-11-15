from django.contrib import admin
from .models import Question, Tag, VoteAnswer, VoteQuestion, Answer, Profile

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(VoteAnswer)
admin.site.register(VoteQuestion)
admin.site.register(Answer)
admin.site.register(Profile)
