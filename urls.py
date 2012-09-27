from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

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
    
    (r'^question/new$', 'words.views.question_new_tile'),
    (r'^question/(\d+)/details$', 'words.views.question_details_tile'),
    
    (r'^lesson/learn$', 'words.views.learn'),
    (r'^lesson/learn/ask$', 'words.views.ask_question'),
    
    (r'^$', 'words.views.index'),
)
