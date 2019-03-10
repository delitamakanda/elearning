from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.create_event, name='create_event'),
    url(r'^(\d+)/detail/$', views.detail_event, name='detail_event'),
]
