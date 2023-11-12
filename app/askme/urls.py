from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'new_questions'),
    path('/hot/', views.hot, name = 'hot'),
    path('tag/blablabla/', views.tag, name = 'tag'),
    path('question/35/', views.question, name = 'question'),
    path('login/', views.login, name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('ask/', views.ask, name = 'ask'),
    path('settings/', views.settings, name = 'settings'),
]
