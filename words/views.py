'''
Created on 22-09-2012

@author: pawel
'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from forms import UserCreationForm
from words.forms import LessonForm, QuestionForm
from words.models import Lesson, Question
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError

@login_required
def index(request):
    to_learn_list = []
    
    for idx in range(10):
        days_from = "today"
        if idx == 1:
            days_from = "1 day"
        elif idx > 1:
            days_from = "{0} days".format(idx)
        
        to_learn_list.append([days_from, Question.objects.to_learn_in(idx).count()])
        
    return render(request, "index.html", {"to_learn_list": to_learn_list})

def user_registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(True)
            return redirect("words.views.index")
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
    
    questions = Question.objects.filter(lesson = lesson)
    
    return render(request, "words/lesson_details.html", {'lesson': lesson, 'questions': questions})

@login_required
def new_lesson(request):
    if request.method == "POST":
        form = LessonForm(request.user, request.POST)
        if form.is_valid():
            form.save(True)
            return redirect("words.views.lesson_list")
    else:
        form = LessonForm(request.user)
        
    return render(request, "words/lesson_form.html", {'form': form})

@login_required
def question_new_tile(request):
    lesson = fetch_lesson_from_session(request)
    if lesson == None:
        return redirect(reverse("words.views.lesson_list"))
    
    if request.method == "POST":
        form = QuestionForm(lesson, request.POST)
        
        if form.is_valid():
            saved_queston =  form.save(True)
            return redirect("words.views.question_details_tile", saved_queston.id)
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
    lesson = fetch_lesson_from_session(request)
    if lesson == None:
        return HttpResponseServerError()
    
    question = Question.objects.get(lesson = lesson, id = question_id)
    
    return render(request, "words/question_details_tile.html", {'question': question})

@login_required
def learn(request):
    questions_to_learn = Question.objects.to_learn_in(0)
    learning_bunch = LearningBunch(questions_to_learn)
    
    request.session['learning_bunch'] = learning_bunch
    
    return render(request, "words/learn.html", {'learning_bunch': learning_bunch})

@login_required
def ask_question(request):
    learning_bunch = request.session.get('learning_bunch', None)
    question = learning_bunch.current_question()
    
    return render(request, "words/next_question.html", {'learning_bunch': learning_bunch, 'question': question})

class LearningBunch:
    
    def __init__(self, questions_to_learn):
        self.bunch = len(questions_to_learn)
        self.passed = 0
        self.current = 0
        
        self.items = []
        for question in questions_to_learn:
            self.items.append(LearningItem(question))
            
    def current_question(self):
        return self.items[self.current]
    
    def __repr__(self):
        return "Learning bund of {0} questions.".format(self.bunch)
            
class LearningItem:
    
    def __init__(self, question):
        self.question = question
        self.score = 0
    
    def __repr__(self):
        return "Question to ask of score {1}: {0}".format(self.question, self.score)
    
    def color(self):
        if self.score == 0:
            return "red"
        elif self.score == 1:
            return "red"
        elif self.score == 2:
            return "red"
        elif self.score == 3:
            return "pink"
        elif self.score == 4:
            return "green"
        elif self.score == 5:
            return "green"
         