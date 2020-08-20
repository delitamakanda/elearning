from django.conf.urls import url
from django.views.generic import TemplateView
from termsandconditions.decorators import terms_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.CourseListView.as_view(), name='course_list'),
    url(r'^dashboard/$', views.ManageCourseListView.as_view(), name='manage_course_list'),
    url(r'^create/$', never_cache(login_required(terms_required(views.CourseCreateView.as_view()))), name='course_create'),
    url(r'^(?P<pk>\d+)/edit/$', views.CourseUpdateView.as_view(), name='course_edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.CourseDeleteView.as_view(), name='course_delete'),
    url(r'^(?P<pk>\d+)/module/$', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/create/$', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/(?P<id>\d+)/$', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    url(r'^content/(?P<id>\d+)/delete/$', views.ContentDeleteView.as_view(), name='module_content_delete'),
    url(r'^module/(?P<module_id>\d+)/$', views.ModuleContentListView.as_view(), name='module_content_list'),
    url(r'^module/order/$', views.ModuleOrderView.as_view(), name='module_order'),
    url(r'^content/order/$', views.ContentOrderView.as_view(), name='content_order'),
    url(r'^subject/(?P<subject>[\w-]+)/$', views.CourseListView.as_view(), name='course_list_subject'),
    url(r'^(?P<slug>[\w-]+)/$', views.CourseDetailView.as_view(), name='course_detail'),
    url(r'^(?P<subject>[\w-]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^videos$', views.list_videos, name='videos_list'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^about-company$', TemplateView.as_view(template_name='about.html'), name='about_company'),
    url(r'^termsrequired$', never_cache(terms_required(login_required(TemplateView.as_view(template_name='terms_required.html')))), name='terms_required'),
    url(r'^search$', views.SearchSubmitView.as_view(), name='search'),
    url(r'^search-ajax-submit$', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
]
