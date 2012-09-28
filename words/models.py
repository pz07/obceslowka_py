'''
Created on 22-09-2012

@author: pawel
'''
from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField
from djangotoolbox.fields import ListField
import datetime

class Lesson(models.Model):
    name = models.CharField(max_length = 32)
    created_at = models.DateTimeField()
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return "{0}".format(self.name)

class AnswerField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, CharField, **kwargs)

class QuestionManager(models.Manager):
    def to_learn_in(self, days):
        now = datetime.datetime.now()
    
        midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=days+1)
        
        if days > 0:
            tomorrow_midnight = midnight + datetime.timedelta(days=1)
            return self.filter(next_repeat__lt = tomorrow_midnight, next_repeat__gte = midnight)
        else:
            return self.filter(next_repeat__lte = midnight)
    
class Question(models.Model):
    objects = QuestionManager()
    
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
    
    def score(self, score):
        #TODO
        pass
    
    def __unicode__(self):
        return u"{0}".format(self.question)
    
class Answer(models.Model):
    answer = models.CharField(max_length = 1024)
    tip = models.CharField(max_length = 1024)
    image_url = models.URLField()
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return "{0}".format(self.answer)

    
    