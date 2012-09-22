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