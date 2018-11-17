import re

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from courses.models import Course

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
    # if request.user.is_authenticated:
    #     if request.user.is_teacher:
    #         return redirect('teacher_quiz_change_list')
    #     else:
    #         return redirect('student_quiz_list')

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
