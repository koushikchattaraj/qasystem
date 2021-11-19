from rest_framework import serializers
from .models import Question

class QuestionSerilizers(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'title', 'user', 'details'] 
    
    # def get_user(self, obj):
    #     user_name = obj.user.username
    #     return user_name