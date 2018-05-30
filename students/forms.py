from django import forms
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
