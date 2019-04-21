from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^liste/$', views.liste_events, name='liste_events'),
    url(r'^listes/$', views.ListEvents.as_view(paginate_by=5), name='listes_events'),
    url(r'^listes/(?P<champ>[\w-]+)/(?P<terme>[\w-]+)/$', views.ListEvents.as_view(paginate_by=5), name='listes_events_filter'),
    url(r'^create/$', views.create_event, name='create_event'),
    url(r'^(\d+)/detail/$', views.detail_event, name='detail_event'),
    url(r'^(\d+)/guest/(\d+)/delete/$', views.delete_guest, name='delete_guest'),
    url(r'^(\d+)/delete/$', views.delete_event, name='delete_event'),
    url(r'^(\d+)/update/$', views.update_event, name='update_event'),
]
