'''
Created on 23-09-2012

@author: pawel
'''
from django.forms.widgets import MultiWidget, TextInput

class AnswerWidget(MultiWidget):
    
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (TextInput(attrs=attrs),
                   TextInput(attrs=attrs),
                   TextInput(attrs=attrs)
                )
        super(AnswerWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.answer, value.tip, value.image_url]
        return [None, None, None]
    
class HiddenAnswerWidget(AnswerWidget):
    is_hidden = True

    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(AnswerWidget, self).__init__(attrs, date_format, time_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True
