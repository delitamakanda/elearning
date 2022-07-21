from decouple import config
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from students.forms import ContactForm
from students.models import User
from django.core.mail import EmailMessage
from django.template import loader
from django.contrib import messages
from django.utils.translation import gettext as _


class SignupView(TemplateView):
    template_name = 'registration/signup.html'


def index(request):
    if request.user.is_authenticated:
         if request.user.is_teacher:
             return redirect('students:teacher_quiz_change_list')
         else:
             return redirect('students:student_quiz_list')
    else:
        return redirect('courses:course_list')


def contact_us_view(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('form_content', '')
            template = loader.get_template('students/contact/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content
            }
            content = template.render(context)

            email = EmailMessage(
                _('Nouveau message de myealearning'),
                content,
                _('myealearning'),
                [config('ADMIN_EMAIL')],
                headers = { 'Reply-To': contact_email }
            )
            email.send()
            messages.success(request, _('Thank you ! We will check in as soon as possible ;-)'))
            return redirect('students:contact_us')
        else:
            messages.info(request, _('Oops ! Message not send...'))
    return render(request, 'students/contact/contact_form.html', { 'form': form_class })


def user_detail(request, username):
    ouser = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'students/user/detail.html', {'ouser': ouser})