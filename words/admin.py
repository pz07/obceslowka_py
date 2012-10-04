from django.contrib import admin
from words.models import Lesson, Question, Answer, Iteration

admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Iteration)