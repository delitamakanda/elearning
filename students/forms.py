from django import forms
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from courses.models import Course
from students.models import (
    Answer,
    Question,
    Student,
    StudentAnswer,
    Tag,
    User
)

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)


class TeacherSignupForm(UserCreationForm):
    username = forms.CharField(label='', widget = forms.TextInput(attrs={'class':'flex-grow h-8 mt-4 px-2 rounded border border-gray-400', 'placeholder':'Username'}))
    email = forms.EmailField(required = True,label='', widget=forms.TextInput(attrs={'class':'flex-grow mt-4 h-8 px-2 rounded border border-gray-400', 'placeholder': 'E-mail'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'flex-grow h-8 mt-4  px-2 rounded border border-gray-400', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'flex-grow h-8 mt-4 px-2 rounded border border-gray-400', 'placeholder': 'Password verification'}))

    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            raise forms.ValidationError("Email or Username exists")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class StudentSignupForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'flex-grow h-8  mt-4  px-2 rounded border border-gray-400', 'placeholder': 'Username'}))
    email = forms.EmailField(required = True,label='', widget=forms.TextInput(attrs={'class':'flex-grow h-8  mt-4  px-2 rounded border border-gray-400','placeholder': 'E-mail'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'flex-grow h-8 mt-4  px-2 rounded border border-gray-400', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'flex-grow h-8 mt-4  px-2 rounded border border-gray-400', 'placeholder': 'Password verification'}))
    interests = forms.ModelMultipleChoiceField(
        label='',
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class':'mt-4 form-control'}),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            raise forms.ValidationError("Email or Username exists")
        return self.cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.email = self.cleaned_data['email']
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentInterestsForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('interests',)
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    # text = forms.CharField(label="Question", widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Question
        fields = ('text',)


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.all(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None
    )

    class Meta:
        model = StudentAnswer
        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args,**kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class ContactForm(forms.Form):
    contact_name = forms.CharField(label="Your name", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    contact_email = forms.EmailField(label="Your email address", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    form_content = forms.CharField(label="Your message", required=True, widget=forms.Textarea(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = 'Your name:'
        self.fields['contact_email'].label = 'Your email address:'
        self.fields['form_content'].label = 'Subject of your message:'
