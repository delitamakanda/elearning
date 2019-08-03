from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^liste/$', views.liste_events, name='liste_events'),
    url(r'^listes/$', views.ListEvents.as_view(paginate_by=5), name='listes_events'),
    url(r'^(?P<pk>\d+)/detail/$', views.DetailEventView.as_view(), name='detail_event'),
    url(r'^listes/(?P<champ>[\w-]+)/(?P<terme>[\w-]+)/$', views.ListEvents.as_view(paginate_by=5), name='listes_events_filter'),
    url(r'^create/$', views.create_event, name='create_event'),
    url(r'^contacts/$', views.ContactListView.as_view(), name='all_contacts'),
    url(r'^contact/(?P<pk>\d+)/$', views.ContactDetailView.as_view(), name='contact_detail'),
    url(r'^circle/(?P<pk>\d+)/$', views.CircleDetailView.as_view(), name='circle_detail'),
    url(r'^(\d+)/guest/(\d+)/delete/$', views.delete_guest, name='delete_guest'),
    url(r'^(\d+)/delete/$', views.delete_event, name='delete_event'),
    url(r'^(\d+)/update/$', views.update_event, name='update_event'),
    url(r'^contact/(?P<pk>\d+)/update/$', views.UserInfoUpdateView.as_view(), name="contact_update"),
    url(r'^contact/(?P<pk>\d+)/delete/$', views.DeleteContactView.as_view(),name='contact_delete'),
    url(r'^invitation/liste/$', views.InvitationListView.as_view(), name='invitation_list'),
    url(r'^invitation/$', views.InvitationCreateView.as_view(), name='create_invitation'),
    url(r'^participation/(?P<pk>\d+)/$', views.UpdateGuestView.as_view(), name='participation_form'),
    url(r'^circle/create/', views.CircleCreateView.as_view(), name='create_circle'),
    url(r'^$', TemplateView.as_view(template_name='calendar/index.html'), name='calendar'),
]
