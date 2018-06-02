from django.conf.urls import url, include
from .views import students, classroom, teachers
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^classroom/$', classroom.index, name='classroom'),

    url(r'^register/student/$', students.StudentRegistrationView.as_view(), name='student_registration'),
    url(r'^enroll-course/$', students.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    url(r'^courses/$', students.StudentCourseListView.as_view(), name='student_course_list'),
    url(r'^course/(?P<pk>\d+)/$', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail'),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail_module'),
    url(r'^quiz-list/$', students.QuizListView.as_view(), name='student_quiz_list'),
    url(r'^interests/$', students.StudentInterestsView.as_view(), name='student_interests'),
    url(r'^taken/$', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
    url(r'^quiz/(?P<pk>\d+)/$', students.take_quiz, name='take_quiz'),
]
