'''
Created on 22-09-2012

@author: pawel
'''
from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField
from djangotoolbox.fields import ListField

class Lesson(models.Model):
    name = models.CharField(max_length = 32)
    created_at = models.DateTimeField()
    user = models.ForeignKey(User)

class AnswerField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, CharField, **kwargs)
    
class Question(models.Model):
    question = models.CharField(max_length = 1024)
    tip = models.CharField(max_length = 1024, blank = True)
    image_url = models.URLField(blank = True)
    created_at = models.DateTimeField()
    level = models.IntegerField()
    next_repeat = models.DateTimeField()
    to_repeat = models.BooleanField()
    lesson = models.ForeignKey(Lesson)
    
    def answers(self):
        return Answer.objects.filter(question = self)
    
class Answer(models.Model):
    answer = models.CharField(max_length = 1024)
    tip = models.CharField(max_length = 1024)
    image_url = models.URLField()
    question = models.ForeignKey(Question)

    
    