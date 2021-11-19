from django.db import models
from django.contrib.auth import get_user_model
from questions.models import Question
User = get_user_model()
from django import template
from ckeditor.fields import RichTextField
register = template.Library()


class Answer(models.Model):
    text = RichTextField()
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

 

    class Meta:
        order_with_respect_to = 'question'
