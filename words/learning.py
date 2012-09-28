'''
Created on 28-09-2012

@author: pawel
'''
from words.matching import match_answers

class LearnMode():
    
    def scored(self, question, score):
        return question.scored(score)
    
    def next_current(self, current, items):
        if current == len(items) -1:
            return -1
        else:
            return current +1

class RepeatMode():

    def scored(self, question, score):
        return question.repeated(score)

    def next_current(self, current, items):
        next_current = -1
        for current_candidate in range(current + 1, len(items)) + range(0, current +1):
            if items[current_candidate].to_learn():
                next_current = current_candidate
                break
            
        return next_current

class LearningBunch:
    
    def __init__(self, questions_to_learn, mode = "learn"):
        self.stats = LearningStats(questions_to_learn)
        self.current = 0
        
        self.items = []
        for question in questions_to_learn:
            self.items.append(LearningItem(question))
            
        if mode == "repeat":
            self.mode = RepeatMode()
        else:
            self.mode = LearnMode()
            
    def current_question(self):
        return self.items[self.current]
    
    def check(self, student_answer):
        question = self.current_question()
        return question.check(student_answer)
    
    def score_question(self, score):
        self.stats.scored(score)
        
        question = self.current_question()
        return self.mode.scored(question, score)
        
    def next_question(self):
        current = self.mode.next_current(self.current, self.items)
        
        if current == -1:
            return None
        else:
            self.current = current
            return self.current_question()
    
    def __repr__(self):
        return u"Learning bund of {0} questions.".format(self.bunch)
    
class LearningStats():
    
    def __init__(self, questions_to_learn):
        self.to_learn = len(questions_to_learn)
        self.score_of = [0, 0, 0, 0, 0, 0, 0]
        
    def scored(self, score):
        if(self.to_learn > 0):
            self.to_learn = self.to_learn -1
            
        self.score_of[score] = self.score_of[score] +1

    def stats(self):
        return {"to learn: ": self.to_learn,
                "score of 0": self.score_of[0], 
                "score of 1": self.score_of[1], 
                "score of 2": self.score_of[2], 
                "score of 3": self.score_of[3], 
                "score of 4": self.score_of[4], 
                "score of 5": self.score_of[5]}

class AnswerResult():
    
    def __init__(self, correct, ratio, best_matching):
        self.correct = correct
        self.ratio = ratio
        self.best_matching = best_matching
        
    def __repr__(self):
        return u"Answer result: {0}".format(self.correct)

class LearningItem:
    
    def __init__(self, question):
        self.question = question
        self.score = 0
    
    def __repr__(self):
        return "Question to ask of score {1}: {0}".format(self.question, self.score)
    
    def check(self, student_answer):
        best_matching = None
        for answer in self.question.answers():
            matching = match_answers(student_answer, answer.answer)
            if best_matching == None or best_matching[0] < matching[0]:
                best_matching = matching
                
            if matching[0] == 100:
                break 
                
        return AnswerResult(best_matching[0] == 100, best_matching[0], best_matching[1:])
    
    def scored(self, score):
        self.score = score
        self.question.score(score);
        
        return self
    
    def repeated(self, score):
        self.score = score
        self.question.repeated(score);
        
        return self
        
    def to_learn(self):
        return self.score < 4
    
    def id(self):
        #TODO zmienic na hash
        return self.question.id    
        
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
