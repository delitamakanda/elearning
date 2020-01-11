import re

from decouple import config
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from courses.models import Course
from students.forms import ContactForm
from students.models import User
from django.core.mail import EmailMessage, send_mail, mail_admins
from django.template import Context, loader
from django.contrib import messages
from django.utils.translation import gettext as _

def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile('\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


class SignupView(TemplateView):
    template_name = 'registration/signup.html'


def index(request):
    if request.user.is_authenticated:
         if request.user.is_teacher:
             return redirect('teacher_quiz_change_list')
         else:
             return redirect('student_quiz_list')
    else:
        return redirect('course_list')


def search(request):
    query_string = ''
    found_results = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        result_query = get_query(query_string, ['title', 'overview', ])
        found_results = Course.objects.filter(result_query).order_by('-created')

    return render(request, 'students/index.html', {
        'query_string': query_string,
        'found_results': found_results
    })


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
            return redirect('contact_us')
        else:
            messages.info(request, _('Oops ! Message not send...'))
    return render(request, 'students/contact/contact_form.html', { 'form': form_class })


def notifications_list(request):
    return render(request, 'students/notifications/list.html', {})


def messages_list(request):
    return render(request, 'students/messages/list.html', {})

def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'students/user/detail.html', {'user': user})