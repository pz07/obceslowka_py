from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic.list import ListView
from words.models import Lesson

handler500 = 'djangotoolbox.errorviews.server_error'

admin.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^accounts/register$', 'words.views.user_registration'),
    
    (r'^lessons/$', 'words.views.lesson_list'),
    (r'^lessons/new$', 'words.views.new_lesson'),
    
    (r'^$', 'words.views.index'),
)
