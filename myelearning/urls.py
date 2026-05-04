"""myelearning URL Configuration for Django 6."""
from django.urls import include, path, re_path
from django.conf import settings
from django.views import generic
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from apps.students.views import classroom

from django.views.generic import TemplateView

urlpatterns = [
    path('', generic.RedirectView.as_view(url='/course/', permanent=True)),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', classroom.SignupView.as_view(), name='signup'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),

    path('course/', include(('apps.courses.urls', 'courses'))),
    path('students/', include(('apps.students.urls', 'students'))),

    path('api/', include(('apps.courses.api.urls', 'api'), namespace='api')),

    path('sw.js', TemplateView.as_view(template_name="service-worker.js", content_type='application/javascript'), name='sw.js'),
    path('offline.html', TemplateView.as_view(template_name="offline.html"), name='offline.html'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
