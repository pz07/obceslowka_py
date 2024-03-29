'''
Created on 22-09-2012

@author: pawel
'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from words.forms import LessonForm, QuestionForm, UserCreationForm
from words.models import Lesson, Question
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
def index(request):
    to_learn_list = []
    
    for idx in range(10):
        days_from = "today"
        if idx == 1:
            days_from = "1 day"
        elif idx > 1:
            days_from = "{0} days".format(idx)
        
        to_learn_list.append([days_from, Question.objects.to_learn_in_count(request.user, idx)])
        
    return render(request, "index.html", {"to_learn_list": to_learn_list, "to_repeat_today": Question.objects.to_repeat_count(request.user)})

def user_registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(True)
            return redirect("words.views.manage.index")
    else:
        form = UserCreationForm()
        
    return render(request, "registration/registration.html", {'form': form})

@login_required
def lesson_list(request):
    lessons = Lesson.objects.filter(user = request.user)
    return render(request, "words/lesson_list.html", {'lessons': lessons})

@login_required
def lesson_details(request, lesson_id):
    lesson = Lesson.objects.get(user = request.user, id = lesson_id)
    request.session["lesson_id"] = lesson.id
    
    paginator = Paginator(Question.objects.filter(lesson = lesson), 25) 

    page = request.GET.get('page')
    if not page:
        page = 1
    
    try:
        question_page = paginator.page(page)
    except PageNotAnInteger:
        question_page = paginator.page(1)
    except EmptyPage:
        question_page = paginator.page(paginator.num_pages)

    return render(request, "words/lesson_details.html", {'lesson': lesson, 'question_page': question_page})

@login_required
def new_lesson(request):
    if request.method == "POST":
        form = LessonForm(request.user, request.POST)
        if form.is_valid():
            form.save(True)
            return redirect("words.views.manage.lesson_list")
    else:
        form = LessonForm(request.user)
        
    return render(request, "words/lesson_form.html", {'form': form})

@login_required
def question_new_tile(request):
    lesson = fetch_lesson_from_session(request)
    if lesson == None:
        return redirect(reverse("words.views.manage.lesson_list"))
    
    if request.method == "POST":
        form = QuestionForm(lesson, request.POST)
        
        if form.is_valid():
            saved_queston =  form.save(True)
            return redirect("words.views.manage.question_details_tile", saved_queston.id)
    else:
        form = QuestionForm(lesson)
        
    return render(request, "words/question_form_tile.html", {'form': form})

def fetch_lesson_from_session(request):
    lesson_id = request.session.get("lesson_id", None)
    if lesson_id == None:
        return None
    
    return Lesson.objects.get(id = lesson_id)

@login_required
def question_details_tile(request, question_id):
    return get_question_details_model(request, question_id, "words/question_details_tile.html")

@login_required
def question_details(request, question_id):
    return get_question_details_model(request, question_id, "words/question_details.html")

def get_question_details_model(request, question_id, view):
    question = Question.objects.get(id = question_id)
    
    if not question.lesson.belongs_to_user(request.user):
        return HttpResponseServerError()
    
    return render(request, view, {'question': question})
                  