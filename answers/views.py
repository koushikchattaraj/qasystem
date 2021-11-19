from functools import partial
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Answer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serilizers import AnswerSerilizers, AnswerPostSerilizers
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class AnswerView(APIView):
    """
        Answer Rest Framework
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    context = {}
    def get(self, request):
        answer = Answer.objects.all()
        answer_serilizers = AnswerSerilizers(answer, many=True)
        self.context['status'] = status.HTTP_200_OK
        self.context['data'] = answer_serilizers.data
        return Response(self.context, status=status.HTTP_200_OK)
    def post(self, request):
        if request.user.is_authenticated:
            request.data.update({"user":request.user.id})
        answer_serilizers = AnswerPostSerilizers(data=request.data)
        if answer_serilizers.is_valid():
            answer_serilizers.save()
            self.context['status'] = status.HTTP_200_OK
            self.context['data'] = answer_serilizers.data
            self.context['message'] = "Your answer is sucessfully save"
            return Response(self.context, status=status.HTTP_200_OK)
        else:
            self.context['status'] = status.HTTP_400_BAD_REQUEST
            self.context['data'] = answer_serilizers.errors
            self.context['message'] = "Somthing went wrong!!"
            return Response(self.context, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        if request.user.is_authenticated:
            request.data.update({"user":request.user.id})
        answer_id = Answer.objects.get(id=pk)
        answer = JSONParser().parse(request)
        answer_serilizers = AnswerSerilizers(answer_id, data=answer, partial=True)
        if answer_serilizers.is_valid():
            answer_serilizers.save()
            self.context['status'] = status.HTTP_200_OK
            self.context['message'] = "Answer is scucessfully Updated"
            return Response(self.context, status=status.HTTP_200_OK)
        else:
            self.context['status'] = status.HTTP_400_BAD_REQUEST
            self.context['message'] = "Smothing went wrong!!"
            return Response(self.context, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        try:
            answer = Answer.objects.get(id=pk)
            answer.delete()
            self.context['status'] = status.HTTP_200_OK
            self.context['message'] = "Answer is scucessfully Deleted"
            return Response(self.context, status=status.HTTP_200_OK)
        except:
            self.context['status'] = status.HTTP_400_BAD_REQUEST
            self.context['message'] = "No answer found to deleted"
            return Response(self.context, status=status.HTTP_400_BAD_REQUEST)
