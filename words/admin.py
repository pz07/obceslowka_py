from django.contrib import admin
from words.models import Lesson, Question, Answer

admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Answer)