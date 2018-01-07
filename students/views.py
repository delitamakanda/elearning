from django.conf import settings
import stripe
import datetime
stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .forms import CourseEnrollForm
from courses.models import Course
from django.core.mail import mail_admins
from django.core import management
from django.contrib import messages

management.call_command('enroll_reminder', days=20)


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            #get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            #get first module
            context['module'] = course.modules.all()[0]
        context['key'] = settings.STRIPE_LIVE_PUBLIC_KEY
        return context


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])


@login_required
def charge(request):
    user = request.user
    course = None

    try:
        customer = stripe.Customer.create(
            email=request.POST['stripeEmail'],
            source=request.POST['stripeToken'],
            plan='monthly',
        )
    except stripe.StripeError as e:
        msg = "Stripe payment error: %s" % e
        messages.error(request, msg)
        mail_admins("Error on myelearning app", msg)
        return redirect('student_course_list')

    if request.method != "POST":
        return redirect('student_course_list')

    if not 'stripeToken' in request.POST:
        messages.error(request, 'Something went wrong !')
        return redirect('student_course_list')

    course.upgraded = True
    course.stripe_id = customer.id
    course.save()

    messages.success(request, 'Upgraded your account. Thanks a lot!')
    return redirect('student_course_list')
