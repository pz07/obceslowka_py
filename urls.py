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
    
    (r'^lesson/list$', 'words.views.lesson_list'),
    (r'^lesson/new$', 'words.views.new_lesson'),
    (r'^lesson/(\d+)', 'words.views.lesson_details'),
    
    (r'^$', 'words.views.index'),
)
