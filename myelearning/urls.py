"""myelearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.views import generic
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from students.views import students, classroom, teachers

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(url='/course/', permanent=True)),

    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^accounts/signup/$', classroom.SignupView.as_view(), name='signup'),
    url(r'^password-change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password-change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password-reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^course/', include(('courses.urls', 'courses'))),
    url(r'^students/', include(('students.urls', 'students'))),

    url(r'^terms/', include(('termsandconditions.urls', 'termsandconditions'))),

    url(r'^api/', include(('courses.api.urls', 'api'), namespace='api')),

    url(r'^sw.js', (TemplateView.as_view(template_name="service-worker.js", content_type='application/javascript', )), name='sw.js'),
    url(r'^offline.html', (TemplateView.as_view(template_name="offline.html")), name='offline.html'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
