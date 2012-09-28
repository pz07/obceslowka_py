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
    
    return render(request, "learn/learn.html", {'learning_bunch': learning_bunch})

@login_required
def ask_question(request):
    learning_bunch = request.session.get('learning_bunch', None)
    question = learning_bunch.current_question()
    
    return render(request, "learn/next_question.html", {'learning_bunch': learning_bunch, 'question': question})

@login_required
def check(request):
    answer = request.POST['answer']
    
    learning_bunch = request.session.get('learning_bunch', None)
    question = learning_bunch.current_question()
    
    result = learning_bunch.check(answer)
    
    return render(request, "learn/check.html", {'result': result, 'learning_bunch': learning_bunch, 'question': question})

@login_required
def score(request, score):
    learning_bunch = request.session.get('learning_bunch', None)
    
    scored_question = learning_bunch.score_question(score)
    question = learning_bunch.next_question()
    
    request.session.modified = True
    
    if question:
        return render(request, "learn/next_question.html", {'learning_bunch': learning_bunch, 'question': question, 'scored_question': scored_question})
    else:
        return render(request, "learn/end.html", {'learning_bunch': learning_bunch, 'scored_question': scored_question})

