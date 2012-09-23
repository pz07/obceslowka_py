'''
Created on 22-09-2012

@author: pawel
'''
from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    name = models.CharField(max_length = 32)
    created_at = models.DateTimeField()
    user = models.ForeignKey(User)
    
class Question(models.Model):
    question = models.CharField(max_length = 1024)
    tip = models.CharField(max_length = 1024)
    image_url = models.URLField()
    created_at = models.DateTimeField()
    level = models.IntegerField()
    next_repeat = models.DateTimeField()
    lesson = models.ForeignKey(Lesson)
    