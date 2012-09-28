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
