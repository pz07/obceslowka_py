'''
Created on 22-09-2012

@author: pawel
'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from words.models import Question
from words.learning import LearningBunch

@login_required
def learn(request, lesson_id = None, days = 0, mode = 'learn'):
    if not days:
        days = 0
    if not lesson_id:
        lesson_id = None
        
    return render_learn_view(request, Question.objects.to_learn_in(int(days), lesson_id), mode)

@login_required
def repeat(request, mode = 'repeat'):
    return render_learn_view(request, Question.objects.to_repeat(), mode)

def render_learn_view(request, questions_to_learn, mode = "learn"):
    to_learn = map(lambda item: item, questions_to_learn)
    
    import random
    random.shuffle(to_learn)
    
    learning_bunch = LearningBunch(to_learn, mode)
    
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
    
    scored_question = learning_bunch.score_question(int(score))
    question = learning_bunch.next_question()
    
    request.session.modified = True
    
    if question:
        return render(request, "learn/next_question.html", {'learning_bunch': learning_bunch, 'question': question, 'scored_question': scored_question})
    else:
        return render(request, "learn/end.html", {'learning_bunch': learning_bunch, 'scored_question': scored_question})

