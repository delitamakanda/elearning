from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name='event_list'),
    url(r'^(?P<pk>\d+)/$', views.EventDetailView.as_view(), name='event_detail'),
]
