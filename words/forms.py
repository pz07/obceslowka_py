'''
Created on 22-09-2012

@author: pawel
'''
from django import forms
from django.contrib.auth.models import User
from words.models import Lesson, Question, Answer
import datetime
from django.forms.util import ErrorList
from words.widgets import AnswerWidget, HiddenAnswerWidget
from django.forms.fields import MultiValueField, CharField,\
    URLField
from django.core import validators
from django.core.exceptions import ValidationError

class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(label= "E-mail")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
        help_text = "Enter the same password as above, for verification.")
    
    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that e-mail already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class LessonForm(forms.ModelForm):
    
    class Meta:
        model = Lesson
        fields = ('name',)

    def __init__(self, user, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        super(LessonForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance)
        self.user = user

    def clean_name(self):
        #per user!!!
        name = self.cleaned_data["name"]
        try:
            Lesson.objects.get(name=name)
        except Lesson.DoesNotExist:
            return name
        raise forms.ValidationError("A lesson with that name already exists.")

    def save(self, commit=True):
        lesson = super(LessonForm, self).save(commit=False)
        lesson.created_at = datetime.datetime.now()
        lesson.user = self.user
        
        if commit:
            lesson.save()
        
        return lesson

class AnswerField(MultiValueField):
    widget = AnswerWidget
    hidden_widget = HiddenAnswerWidget
    default_error_messages = {
        'invalid_date': u'Enter a valid date.',
        'invalid_time': u'Enter a valid time.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
            CharField(error_messages={'invalid': errors['invalid_date']},
                      localize=localize),
            CharField(error_messages={'invalid': errors['invalid_time']},
                      localize=localize, required = False),
            URLField(error_messages={'invalid': errors['invalid_time']},
                      localize=localize, required = False)
        )
        super(AnswerField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            
            result = Answer()
            result.answer = data_list[0]
            result.tip = data_list[1]
            result.image_url = data_list[2]
            
            return result
        
        return None
        
class QuestionForm(forms.ModelForm):
    answer0 = AnswerField(required = True)
    answer1 = AnswerField(required = False)
    answer2 = AnswerField(required = False)
    answer3 = AnswerField(required = False)
    answer4 = AnswerField(required = False)
    answer5 = AnswerField(required = False)
    answer6 = AnswerField(required = False)
    answer7 = AnswerField(required = False)
    answer8 = AnswerField(required = False)
    answer9 = AnswerField(required = False)
    
    class Meta:
        model = Question
        fields = ('question', 'tip', 'image_url')
        
    def __init__(self, lesson, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False):
        super(QuestionForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted)
        self.lesson = lesson
                
    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.lesson = self.lesson
        
        now = datetime.datetime.now()
        
        question.created_at = now
        question.level = 1
        question.next_repeat = now + datetime.timedelta(days=1)
        question.to_repeat = True
        
        if commit:
            question.save()
            
            for idx in range(10):
                answer = self.cleaned_data['answer'+str(idx)]
                if answer:
                    answer.question = question
                    answer.save()
        
        return question
    