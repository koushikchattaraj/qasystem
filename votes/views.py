from questions.models import Question
from answers.models import Answer
import re
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import QuestionVote, AnswerVote
from .serilizers import QuestionSerilizers
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views import View
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status
from accounts.models import User

class QuestionUpVoteApi(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    context = {}

    def get(self, request, pk):
        # questionvote = get_object_or_404(QuestionVote)
        question_vote = QuestionVote.objects.filter(user=request.user.id)
        allvote = QuestionVote.objects.filter(question=pk).count()
        downvote = QuestionVote.objects.filter(question=pk,downvote="1").count()
        totalvote = allvote-downvote
        return Response({'count':totalvote}, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        print("****")
        question = get_object_or_404(Question, pk=pk)
        print(question,"*************")
        users_question_votes = User.objects.prefetch_related('user_question_vote').get(username__iexact=request.user.username)
        print(users_question_votes,"**************")
        if users_question_votes.user_question_vote.all().filter(question = question).exists():
            user_vote_for_this_question = users_question_votes.user_question_vote.all().filter(question = question).get()
            print(user_vote_for_this_question,"******************")
            if user_vote_for_this_question.upvote == True:
                return Response({"Message":"Already Upvoteded this question","count":0})

            if user_vote_for_this_question.downvote == True:
                user_vote_for_this_question.upvote = True
                user_vote_for_this_question.downvote = False
                user_vote_for_this_question.save()
                question.votes += 2
                question.save()
                return Response({"Message":"Sucessfully Updated","count":2})

        new_question_vote = QuestionVote.objects.create_question_vote(request.user, question)
        new_question_vote.upvote = True
        new_question_vote.save()
        question.votes += 1
        question.save()
        return Response({"data":"hi"})

class QuestionDownVoteApi(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    context = {}
    
    def post(self, request, pk):
        print("****")
        question = get_object_or_404(Question, pk=pk)
        print(question,"*************")
        users_question_votes = User.objects.prefetch_related('user_question_vote').get(username__iexact=request.user.username)
        print(users_question_votes,"**************")
        if users_question_votes.user_question_vote.all().filter(question = question).exists():
            user_vote_for_this_question = users_question_votes.user_question_vote.all().filter(question = question).get()
            print(user_vote_for_this_question,"******************")
            if user_vote_for_this_question.downvote == True:
                return Response({"Message":"Already Down Voteded this question","count":0})

            if user_vote_for_this_question.upvote == True:
                user_vote_for_this_question.downvote = True
                user_vote_for_this_question.upvote = False
                user_vote_for_this_question.save()
                question.votes += 2
                question.save()
                return Response({"Message":"Sucessfully Updated","count":2})

        new_question_vote = QuestionVote.objects.create_question_vote(request.user, question)
        new_question_vote.downvote = True
        new_question_vote.save()
        question.votes += 1
        question.save()
        return Response({"data":"hi"})




class AnswerUpVoteApi(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    context = {}

    def get(self, request, pk):
        # questionvote = get_object_or_404(QuestionVote)
        answer_vote = AnswerVote.objects.filter(user=request.user.id)
        allvote = AnswerVote.objects.filter(question=pk).count()
        downvote = AnswerVote.objects.filter(question=pk,downvote="1").count()
        totalvote = allvote-downvote
        return Response({'count':totalvote}, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        print("****")
        answer = get_object_or_404(Answer, pk=pk)
        print(answer,"*************")
        users_answer_votes = User.objects.prefetch_related('user_answer_vote').get(username__iexact=request.user.username)
        print(users_answer_votes,"**************")
        if users_answer_votes.user_answer_vote.all().filter(answer = answer).exists():
            user_vote_for_this_answer = users_answer_votes.user_answer_vote.all().filter(answer = answer).get()
            print(user_vote_for_this_answer,"******************")
            if user_vote_for_this_answer.upvote == True:
                allvote = AnswerVote.objects.filter(answer=pk).count()
                downvote = AnswerVote.objects.filter(answer=pk,downvote="1").count()
                totalvote = allvote-downvote
                return Response({"Message":"Already Upvoteded this question","count":totalvote})

            if user_vote_for_this_answer.downvote == True:
                user_vote_for_this_answer.upvote = True
                user_vote_for_this_answer.downvote = False
                user_vote_for_this_answer.save()
                answer.votes += 2
                answer.save()
                allvote = AnswerVote.objects.filter(answer=pk).count()
                downvote = AnswerVote.objects.filter(answer=pk,downvote="1").count()
                totalvote = allvote-downvote
                return Response({"Message":"Sucessfully Updated","count":totalvote})

        new_answer_vote = AnswerVote.objects.create_answer_vote(request.user, answer)
        new_answer_vote.upvote = True
        new_answer_vote.save()
        answer.votes += 1
        answer.save()
        allvote = AnswerVote.objects.filter(answer=pk).count()
        downvote = AnswerVote.objects.filter(answer=pk,downvote="1").count()
        totalvote = allvote-downvote
        return Response({"data":"hi", "count":totalvote})

class AnswerDownVoteApi(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    context = {}

    def get(self, request, pk):
        # questionvote = get_object_or_404(QuestionVote)
        question_vote = QuestionVote.objects.filter(user=request.user.id)
        allvote = QuestionVote.objects.filter(question=pk).count()
        downvote = QuestionVote.objects.filter(question=pk,downvote="1").count()
        totalvote = allvote-downvote
        return Response({'count':totalvote}, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        print("****")
        answer = get_object_or_404(Answer, pk=pk)
        print(answer,"*************")
        users_answer_votes = User.objects.prefetch_related('user_answer_vote').get(username__iexact=request.user.username)
        print(users_answer_votes,"**************")
        if users_answer_votes.user_answer_vote.all().filter(answer = answer).exists():
            user_vote_for_this_answer = users_answer_votes.user_answer_vote.all().filter(answer = answer).get()
            print(user_vote_for_this_answer,"******************")
            if user_vote_for_this_answer.downvote == True:
                allvote = AnswerVote.objects.filter(answer=pk).count()
                downvote = AnswerVote.objects.filter(answer=pk,downvote="1").count()
                totalvote = allvote-downvote
                return Response({"Message":"Already Upvoteded this question","count":totalvote})

            if user_vote_for_this_answer.upvote == True:
                user_vote_for_this_answer.downvote = True
                user_vote_for_this_answer.upvote = False
                user_vote_for_this_answer.save()
                answer.votes += 1
                answer.save()
                allvote = AnswerVote.objects.filter(answer=pk).count()
                downvote = AnswerVote.objects.filter(answer=pk,downvote="1").count()
                totalvote = allvote-downvote
                return Response({"Message":"Sucessfully Updated","count":totalvote})

        new_answer_vote = AnswerVote.objects.create_answer_vote(request.user, answer)
        new_answer_vote.downvote = True
        new_answer_vote.save()
        answer.votes += 1
        answer.save()
        return Response({"data":"hi"})