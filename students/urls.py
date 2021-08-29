from django.conf.urls import url, include
from .views import students, classroom, teachers
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^classroom/$', classroom.index, name='classroom'),
    url(r'^contact/$', classroom.contact_us_view, name='contact_us'),
    url(r'^users/(?P<username>.+)/$', classroom.user_detail, name='user_detail'),

    url(r'^register/student/$', students.StudentRegistrationView.as_view(), name='student_registration'),
    url(r'^enroll-course/$', students.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    url(r'^courses/$', students.StudentCourseListView.as_view(), name='student_course_list'),
    url(r'^course/(?P<pk>\d+)/$', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail'),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail_module'),
    url(r'^student/quiz/$', students.QuizListView.as_view(), name='student_quiz_list'),
    url(r'^interests/$', students.StudentInterestsView.as_view(), name='student_interests'),
    url(r'^taken/$', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
    url(r'^student/quiz/(?P<pk>\d+)/$', students.take_quiz, name='take_quiz'),

    url(r'^register/teacher/$', teachers.TeacherRegistrationView.as_view(), name='teacher_registration'),
    url(r'^quiz/$', teachers.TeacherQuizListView.as_view(), name='teacher_quiz_change_list'),
    url(r'^quiz/add/$', teachers.QuizCreateView.as_view(), name='teacher_add_quiz'),
    url(r'^quiz/(?P<pk>\d+)/$', teachers.QuizUpdateView.as_view(), name='teacher_update_quiz'),
    url(r'^quiz/(?P<pk>\d+)/delete/$', teachers.QuizDeleteView.as_view(), name='teacher_delete_quiz'),
    url(r'^quiz/(?P<pk>\d+)/results/$', teachers.QuizResultsView.as_view(), name='teacher_quiz_results'),
    url(r'^quiz/(?P<pk>\d+)/question/add/$', teachers.question_add, name='teacher_add_question'),
    url(r'^quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/$', teachers.question_change, name='teacher_change_question'),
    url(r'^quiz/(?P<quiz_pk>\d+)/question/(?P<question_pk>\d+)/delete/$', teachers.QuestionDeleteView.as_view(), name='teacher_delete_question'),
]
