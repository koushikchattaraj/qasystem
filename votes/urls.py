from rest_framework import views
from votes.views import  QuestionUpVoteApi, QuestionDownVoteApi, AnswerUpVoteApi, AnswerDownVoteApi
from django.contrib import admin
from django.urls import path

app_name= 'votes'

urlpatterns = [
    path('api/question/upvote/<int:pk>',QuestionUpVoteApi.as_view(),name="question-up-vote-api"),
    path('api/question/downvote/<int:pk>',QuestionDownVoteApi.as_view(),name="question-down-vote-api"),
    path('api/answer/upvote/<int:pk>',AnswerUpVoteApi.as_view(),name="answer-up-vote-api"),
    path('api/answer/downvote/<int:pk>',AnswerDownVoteApi.as_view(),name="answer-down-vote-api"),

]