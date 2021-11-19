from rest_framework import serializers
from .models import QuestionVote

class QuestionSerilizers(serializers.ModelSerializer):
    class Meta:
        model = QuestionVote
        fields = ['id', 'question', 'user', 'upvote', 'downvote'] 
    