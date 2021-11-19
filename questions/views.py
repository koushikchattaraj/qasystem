from django import template
from django.http import response
import rest_framework
from rest_framework.decorators import permission_classes
from questions.models import Question, User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serilizers import QuestionSerilizers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views import View
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from answers.models import Answer
from answers.serilizers import AnswerSerilizers
from votes.models import AnswerVote

class AllQuestionApiView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    context = {}
    def get(self,request):
        question = Question.objects.all()
        question_serilizers = QuestionSerilizers(question, many=True)
        self.context['status'] = status.HTTP_200_OK
        self.context['data'] = question_serilizers.data
        return Response(self.context, status=status.HTTP_200_OK)

class QuestionApiView(APIView):
    """
        Question rest_framework
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, pk):
        if request.user.is_authenticated:
            question = get_object_or_404(Question, pk=pk)
            answer = Answer.objects.filter(question=question)
            for ans_obj in answer:
                allvote = AnswerVote.objects.filter(answer=ans_obj.pk).count()
                downvote = AnswerVote.objects.filter(answer=ans_obj.pk,downvote="1").count()
                totalvote = allvote-downvote
                ans_obj.votes = totalvote
                ans_obj.save()
            total_ans = answer.count()
            answerserilizers = AnswerSerilizers(answer, many=True)
            question_serilizers = QuestionSerilizers(question)
            return Response({'question':question_serilizers.data,"answers":answerserilizers.data,"total_ans":total_ans}, status=status.HTTP_200_OK)
        else:
            self.context['status'] = status.HTTP_400_BAD_REQUEST
            self.context['Messase'] = "You are not authenticated"
            return Response(self.context, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        context = {}
        if request.user.is_authenticated:
            request.data.update({"user":request.user.id})
        questions_serilizers = QuestionSerilizers(data=request.data)
        if questions_serilizers.is_valid():
            questions_serilizers.save()
            context['status'] = status.HTTP_200_OK
            context['data'] = questions_serilizers.data
            context['message'] = "Question is scucessfully created"
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['data'] = questions_serilizers.errors
            context['message'] = "question is not created"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        context = {}

        try:
            question = Question.objects.get(id=pk)
            question = Question.objects.filter(id=pk,user=request.user.id)
            if question.exists():
                question.delete()
                context['status'] = status.HTTP_200_OK
                context['message'] = "Question is scucessfully Deleted"
                return Response(context, status=status.HTTP_200_OK)
            else:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "Thats not your questions"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "No question found to deleted"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class QuestionView(View):
    template_name = 'ask_question.html'

    def get(self, request):
        
        return render(request, self.template_name)

class QuestionByIdView(View):
    template_name = 'questionbyid.html'

    def get(self, request ,pk):
        
        return render(request, self.template_name)

class allQuestionView(View):
    template_name = 'questions.html'

    def get(self, request):
        
        return render(request, self.template_name)