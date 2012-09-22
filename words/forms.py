'''
Created on 22-09-2012

@author: pawel
'''
from django import forms
from django.contrib.auth.models import User
from words.models import Lesson
import datetime
from django.forms.util import ErrorList

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
    name = forms.CharField(label = "Name")
    
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