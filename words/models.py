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
    updated_at = models.DateTimeField(default = datetime.datetime.now)
    user = models.ForeignKey(User)
    active = models.BooleanField(default = True)
    
    def __unicode__(self):
        return u"{0}".format(self.name)
    
    def question_to_learn_count(self):
        midnight = midnight_x_days_further(0)
        return Question.objects.filter(next_repeat__lte=midnight, lesson = self.id).count()

    def question_count(self):
        return Question.objects.filter(lesson = self.id).count()
    
    def belongs_to_user(self, user):
        return self.user == user

class AnswerField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, CharField, **kwargs)

def midnight_x_days_further(days):
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=days + 1)

class QuestionManager(models.Manager):
    
    def get_question_to_learn_in_filter(self, user, days = 0, lesson_id = None):
        midnight = midnight_x_days_further(days)
    
        if days > 0:
            tomorrow_midnight = midnight + datetime.timedelta(days=1)
            return self.filter(active = True, next_repeat__lt=tomorrow_midnight, next_repeat__gte=midnight, lesson__in = self.get_user_lesson_ids(user, lesson_id))
        else:
            return self.filter(active = True, next_repeat__lte=midnight, lesson__in = self.get_user_lesson_ids(user, lesson_id))
    
    def to_learn_in_count(self, user, days = 0, lesson_id = None):
        return self.get_question_to_learn_in_filter(user, days, lesson_id).count()
    
    def to_learn_in(self, user, days = 0, lesson_id = None, max_count = 50):
        return (self.get_question_to_learn_in_filter(user, days, lesson_id))[0:max_count]
        
    def to_repeat(self, user):
        return self.get_to_repeat_filter(user)
    
    def to_repeat_count(self, user):
        return self.get_to_repeat_filter(user).count()
    
    def get_to_repeat_filter(self, user, lesson_id = None):
        return self.filter(to_repeat=True, lesson__in = self.get_user_lesson_ids(user, lesson_id))
    
    def get_user_lesson_ids(self, user, lesson_id = None, only_active = True):
        if lesson_id:
            lesson = Lesson.objects.get(id = lesson_id)
            if only_active and not lesson.active:
                lesson = None
            
            if lesson and lesson.user == user:
                lesson_ids = [lesson_id]
            else:
                lesson_ids = []
        else: 
            if only_active:
                lessons = Lesson.objects.filter(user = user, active = True)
            else:
                lessons = Lesson.objects.filter(user = user)
                
            lesson_ids = map((lambda lesson: lesson.id), lessons)
        
        return lesson_ids
    
class Question(models.Model):
    objects = QuestionManager()
    
    question = models.CharField(max_length=1024)
    tip = models.CharField(max_length=1024, blank=True)
    answer_tip = models.CharField(max_length=1024, blank=True)
    image_url = models.URLField(blank=True)
    answer_image_url = models.URLField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(default = datetime.datetime.now)
    level = models.IntegerField()
    next_repeat = models.DateTimeField()
    to_repeat = models.BooleanField()
    e_factor = models.FloatField(default=2.5)
    lesson = models.ForeignKey(Lesson)
    last_attempt_date = models.DateTimeField(blank=True,null=True)
    active = models.BooleanField(default=True)
    
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

        if score < 3:
            self.level = 1
            self.next_repeat = datetime.datetime.now() + datetime.timedelta(days=self.current_iteration().day_interval)
        else:
            ci.learning_finished = datetime.datetime.now()
            
            #EF+(0.1-(5-q)*(0.08+(5-q)*0.02))
            self.e_factor = self.e_factor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))

            if self.e_factor < 1.3:
                self.e_factor = 1.3
        
            ni = self.next_iteration(ci)
        
            self.next_repeat = datetime.datetime.now() + datetime.timedelta(days=ni.day_interval)
            
        if score < 4:
            self.to_repeat = True
        
        self.last_attempt_date = datetime.datetime.now()
        
        ci.save()
        
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
        ret.created_at = datetime.datetime.now()
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
        
        if self.level > 9:
            self.active = False
        
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
    learning_finished = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(default = datetime.datetime.now)
    updated_at = models.DateTimeField(default = datetime.datetime.now)
    
    def __unicode__(self):
        return u"Level {0} for {1}".format(self.level, self.question)
    
    def save(self):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        
        self.updated_at = datetime.datetime.now()
        super(Iteration, self).save()
    
class Answer(models.Model):
    answer = models.CharField(max_length=1024)
    tip = models.CharField(max_length=1024)
    question = models.ForeignKey(Question)
    created_at = models.DateTimeField(default = datetime.datetime.now)
    updated_at = models.DateTimeField(default = datetime.datetime.now)

    def save(self):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
            
        self.updated_at = datetime.datetime.now()
        super(Answer, self).save()
    
    def __unicode__(self):
        return "{0}".format(self.answer)

    
    
