from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django import template
register = template.Library()

class Question(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    details = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def answer_count(self):
        question = Question.objects.prefetch_related('answers').get(id=self.pk)
        return question.answers.all().count()

    class Meta:
        ordering = ['created_at']
