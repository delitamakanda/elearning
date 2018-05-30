from django.conf.urls import url, include
from .views import students, classroom, teachers
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^classroom/$', classroom.index, name='classroom'),
    
    url(r'^register/$', students.StudentRegistrationView.as_view(), name='student_registration'),
    url(r'^enroll-course/$', students.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    url(r'^courses/$', students.StudentCourseListView.as_view(), name='student_course_list'),
    url(r'^course/(?P<pk>\d+)/$', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail'),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$', cache_page(60*15)(students.StudentCourseDetailView.as_view()), name='student_course_detail_module'),
]
