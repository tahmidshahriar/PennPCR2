from django.conf.urls import patterns, url
from newcourse import views

urlpatterns = patterns('',
                        url(r'^$', views.index, name='index'),
                        url(r'^about/', views.about, name='about'),
                        url(r'^register/$', views.register, name = 'register'),
                        url(r'^login/$', views.user_login, name='login'),
                        url(r'^logout/$', views.user_logout, name='logout'),
                        url(r'^category/(?P<thetype>\w+)/$', views.deptlist, name='list'),
                        url(r'^category/(?P<thetype>\w+)/(?P<page>\w+)/$', views.proflist, name='list'),
                        url(r'^depts/(?P<thetype>\w+)/$', views.courselist, name='course'),
                        url(r'^instructors/(?P<theid>\w+)/$', views.instructor, name='ins'),
                        url(r'^instructors/(?P<theid>\w+)/comment/$', views.add_profcomment, name='ins'),
                        url(r'^confirm/(?P<activation_key>\w+)/$', views.confirm, name = 'confirm'),
                        url(r'^coursehistories/(?P<theid>\w+)/$', views.coursepage, name='ins'),
                        url(r'^depts/(?P<theid>\w+)/comment/$', views.add_classcomment, name='ins'),
                        url(r'^deletealot/sanjidshahriar/donotdothis/$', views.cleanall, name = 'clean'),
                        )
