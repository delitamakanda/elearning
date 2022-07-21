from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Course
from django.http import HttpResponse
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class SubdomainCourseMiddleware(MiddlewareMixin):
    """
    Provides subdomains for courses
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        host_parts = request.get_host().split('.')
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # get course for the given subdomain
            course = get_object_or_404(Course, slug=host_parts[0])
            course_url = reverse('courses:course_detail', args=[course.slug])
            # redirect current request to the course_detail view
            url = '{}://{}{}'.format(request.scheme, '.'.join(host_parts[1:]), course_url)

            return redirect(url)
