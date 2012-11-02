from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

handler500 = 'djangotoolbox.errorviews.server_error'

admin.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^accounts/register$', 'words.views.manage.user_registration'),
    
    (r'^lesson/list$', 'words.views.manage.lesson_list'),
    (r'^lesson/new$', 'words.views.manage.new_lesson'),
    (r'^lesson/(\d+)', 'words.views.manage.lesson_details'),
    
    (r'^question/new$', 'words.views.manage.question_new_tile'),
    (r'^question/(\d+)/details$', 'words.views.manage.question_details'),
    
    (r'^lesson/learn$', 'words.views.learn.learn'),
    (r'^lesson/learn/lesson/(?P<lesson_id>\d+)$', 'words.views.learn.learn', {}, "learn_lesson"),
    (r'^lesson/learn/days/(?P<days>\d+)$', 'words.views.learn.learn', {}, "learn_in_days"),
    (r'^lesson/repeat$', 'words.views.learn.repeat'),
    (r'^lesson/learn/ask$', 'words.views.learn.ask_question'),
    (r'^lesson/learn/check$', 'words.views.learn.check'),
    (r'^lesson/learn/score/(\d)$', 'words.views.learn.score'),
    
    (r'^tile/question/(\d+)/details$', 'words.views.manage.question_details_tile'),
    
    (r'^$', 'words.views.manage.index'),
)

urlpatterns += staticfiles_urlpatterns()
