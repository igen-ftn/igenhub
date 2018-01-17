from django.conf.urls import url
from igenapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
               #url(r'^$', views.index, name='index'),
               #url(r'(?P<tea>\w+)/$', views.insert, name='insert'),
    url(r'^$', views.home, name='home'),
    url(r'^wiki/$', views.wiki, name='wiki'),
    url(r'^wiki-form/$', views.wiki_form, name='wikiform'),
    url(r'^issues/$', views.issues, name='issues'),
    url(r'^commits/$', views.commits, name='commits'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/profile/$', views.editUser, name='editUser'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
