'''
Created on 28-09-2012

@author: pawel
'''

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
    
    def check(self, student_answer):
        question = self.current_question()
        return question.check(student_answer)
    
    def score_question(self, score):
        question = self.current_question()
        question.scored(int(score))
        
    def next_question(self):
        current = -1
        for current_candidate in range(self.current + 1, len(self.items)) + range(0, self.current +1):
            if self.items[current].to_learn():
                current = current_candidate
                break
        
        if current == -1:
            return None
        else:
            self.current = current_candidate
            return self.current_question()
    
    def __repr__(self):
        return u"Learning bund of {0} questions.".format(self.bunch)

class AnswerResult():
    
    def __init__(self, correct):
        self.correct = correct
        
    def __repr__(self):
        return u"Answer result: {0}".format(self.correct)

class LearningItem:
    
    def __init__(self, question):
        self.question = question
        self.score = 0
    
    def __repr__(self):
        return "Question to ask of score {1}: {0}".format(self.question, self.score)
    
    def check(self, student_answer):
        correct = False
        for answer in self.question.answers():
            if answer.answer == student_answer:
                correct = True
                
        return AnswerResult(correct)
    
    def scored(self, score):
        self.score = score
        self.question.score(score);
        
    def to_learn(self):
        return self.score < 4    
        
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
