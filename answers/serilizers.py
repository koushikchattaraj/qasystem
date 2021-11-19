from re import A
from django.shortcuts import  get_object_or_404
from rest_framework import serializers
from .models import Answer, User
from questions.models import Question
from accounts.serializers import UserSerilizers

class AnswerSerilizers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'text', 'user', 'question', 'votes']

    def get_user(self, obj):
        user_name = obj.user.username
        return user_name


class AnswerPostSerilizers(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'text', 'user', 'question']
 




