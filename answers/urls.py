from .views import  AnswerView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('api/answer/',AnswerView.as_view(),name="answer"),
    path('api/answer/<int:pk>',AnswerView.as_view(),name="answer"),
]