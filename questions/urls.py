from questions.views import  QuestionApiView, QuestionView, AllQuestionApiView, allQuestionView 
from .views import QuestionByIdView
from django.contrib import admin
from django.urls import path

app_name= 'question'

urlpatterns = [
    path('ask-question/',QuestionView.as_view(),name="ask-question"),
    path('questions/',allQuestionView.as_view(),name="all-question"),
    path('api/questions/',QuestionApiView.as_view(),name="QuestionApi"),
    path('api/question/<int:pk>',QuestionApiView.as_view(),name="QuestionApi"),
    path('api/question/get/<int:pk>',QuestionApiView.as_view(),name="Questionget"),
    path('api/questions/',QuestionApiView.as_view(),name="QuestionApi"),
    path('api/all-questions/', AllQuestionApiView.as_view(), name="all-questions"),
    path('questions/<int:pk>', QuestionByIdView.as_view(), name="all-questions"),

]