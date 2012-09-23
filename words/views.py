'''
Created on 22-09-2012

@author: pawel
'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from forms import UserCreationForm
from words.forms import LessonForm
from words.models import Lesson

@login_required
def index(request):
    print "tututu {0}".format(request.user.is_authenticated)
    return render(request, "index.html")

def user_registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(True)
            return redirect("words.views.index")
    else:
        form = UserCreationForm()
        
    return render(request, "registration/registration.html", {'form': form})

def lesson_list(request):
    lessons = Lesson.objects.filter(user = request.user)
    return render(request, "words/lesson_list.html", {'lessons': lessons})

def lesson_details(request, lesson_id):
    lesson = Lesson.objects.get(user = request.user, id = lesson_id)
    return render(request, "words/lesson_details.html", {'lesson': lesson, 'questions': []})

def new_lesson(request):
    if request.method == "POST":
        form = LessonForm(request.user, request.POST)
        if form.is_valid():
            form.save(True)
            return redirect("words.views.lesson_list")
    else:
        form = LessonForm(request.user)
        
    return render(request, "words/lesson_form.html", {'form': form})
    
