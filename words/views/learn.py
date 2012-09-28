'''
Created on 22-09-2012

@author: pawel
'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from words.models import Question
from words.learning import LearningBunch

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