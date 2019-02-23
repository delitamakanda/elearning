from django import forms
from django.forms.models import inlineformset_factory
from courses.models import Course, Module, Review
from students.models import (
    User
)

ModuleFormSet = inlineformset_factory(Course, Module, fields=['title', 'description',], extra=2, can_delete=True)


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('rating', 'comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 40, 'rows': 15, 'class':'form-control'})
        }
