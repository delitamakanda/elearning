from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^post/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^post/like/$', views.post_like, name='post_like'),
]