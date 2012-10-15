'''
Created on 22-09-2012

@author: pawel
'''
from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField
from djangotoolbox.fields import ListField
import datetime
import math

class Lesson(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255, blank=True) 
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default = datetime.datetime.now())
    user = models.ForeignKey(User)
    active = models.BooleanField(default = True)
    
    def __unicode__(self):
        return u"{0}".format(self.name)

class AnswerField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, CharField, **kwargs)

class QuestionManager(models.Manager):
    def to_learn_in(self, days):
        now = datetime.datetime.now()
    
        midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=days + 1)
        
        if days > 0:
            tomorrow_midnight = midnight + datetime.timedelta(days=1)
            return self.filter(next_repeat__lt=tomorrow_midnight, next_repeat__gte=midnight)
        else:
            return self.filter(next_repeat__lte=midnight)
    
    def to_repeat(self):
        return self.filter(to_repeat=True)
    
class Question(models.Model):
    objects = QuestionManager()
    
    question = models.CharField(max_length=1024)
    tip = models.CharField(max_length=1024, blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField()
    level = models.IntegerField()
    next_repeat = models.DateTimeField()
    to_repeat = models.BooleanField()
    e_factor = models.FloatField(default=2.5)
    lesson = models.ForeignKey(Lesson)
    
    def answers(self):
        return Answer.objects.filter(question=self)
    
    def score(self, score):
        ci = self.current_iteration()
        
        if score == 0:
            ci.answers_0 = (ci.answers_0+1)
        elif score == 1:
            ci.answers_1 = (ci.answers_1+1)
        elif score == 2:
            ci.answers_2 = (ci.answers_2+1)
        elif score == 3:
            ci.answers_3 = (ci.answers_3+1)
        elif score == 4:
            ci.answers_4 = (ci.answers_4+1)
        elif score == 5:
            ci.answers_5 = (ci.answers_5+1)

        ci.save()
        
        if score < 3:
            self.level = 1
            self.next_repeat = datetime.datetime.now() + datetime.timedelta(days=self.current_iteration().day_interval)
        else:
            #EF+(0.1-(5-q)*(0.08+(5-q)*0.02))
            self.e_factor = self.e_factor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))

            if self.e_factor < 1.3:
                self.e_factor = 1.3
        
            ni = self.next_iteration(ci)
        
            self.next_repeat = datetime.datetime.now() + datetime.timedelta(days=ni.day_interval)
        
        self.save()
        
    def iterations(self):
        return Iteration.objects.filter(question=self)
        
    def current_iteration(self):
        candidates = Iteration.objects.filter(question=self, level=self.level)
        if len(candidates) > 0:
            return candidates[0]
        else:
            ret = self.create_iteration()
            return ret
        
    def create_iteration(self):
        ret = Iteration()
        
        ret.question = self
        ret.level = self.level
        ret.learning_begin = datetime.datetime.now()
        ret.answers_0 = 0
        ret.answers_1 = 0
        ret.answers_2 = 0
        ret.answers_3 = 0
        ret.answers_4 = 0
        ret.answers_5 = 0    
        ret.day_interval = 1
        
        ret.save()
        
        return ret

    def next_iteration(self, last_iteration):
        self.level = self.level +1
        
        ret = None
        
        candidates = Iteration.objects.filter(question=self, level=self.level)
        if len(candidates) > 0:
            ret = candidates[0]
        else:
            ret = self.create_iteration()
        
        if ret.level == 1:
            ret.day_interval = 1
        elif ret.level == 2:
            ret.day_interval = 4
        else:
            ret.day_interval = math.floor(self.e_factor * last_iteration.day_interval)
        
        ret.save()
            
        return ret
    
    def repeated(self, score):
        if score > 3:
            self.to_repeat = False
            self.save()
    
    def __unicode__(self):
        return u"{0}".format(self.question)
    
class Iteration(models.Model):
    
    question = models.ForeignKey(Question)
    level = models.IntegerField()
    learning_begin = models.DateTimeField()
    day_interval = models.IntegerField(default = 4)
    answers_0 = models.IntegerField()
    answers_1 = models.IntegerField()
    answers_2 = models.IntegerField()
    answers_3 = models.IntegerField()
    answers_4 = models.IntegerField()
    answers_5 = models.IntegerField()
    
    def __unicode__(self):
        return u"Level {0} for {1}".format(self.level, self.question)
    
class Answer(models.Model):
    answer = models.CharField(max_length=1024)
    tip = models.CharField(max_length=1024)
    image_url = models.URLField()
    question = models.ForeignKey(Question)

    def __unicode__(self):
        return "{0}".format(self.answer)

    
    
