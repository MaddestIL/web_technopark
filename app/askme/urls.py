from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('hot/', views.hot_questions, name='hot'),
    path('best/', views.best_questions, name='best_questions'),
    path('ask/', views.new_questions, name='ask'),
    path('tag/<str:tag>', views.tag_questions, name='tag_questions'),
    path('question/<int:question_id>', views.question, name='question')
]