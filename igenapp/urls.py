from django.conf.urls import url
from igenapp import views

urlpatterns = [
               #url(r'^$', views.index, name='index'),
               #url(r'(?P<tea>\w+)/$', views.insert, name='insert'),
    url(r'^$', views.home, name='home'),
    url(r'^wiki/$', views.wiki, name='wiki'),
    url(r'^issues/$', views.issues, name='issues'),
    url(r'^commits/$', views.commits, name='commits'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^users/(?P<id>\d+)/$', views.users, name='users'),
]
