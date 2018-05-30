from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class SignupView(TemplateView):
    template_name = 'registration/signup.html'

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:quiz_change_list')
        else:
            return redirect('students:quiz_list')
    return render(request, 'students/index.html')
