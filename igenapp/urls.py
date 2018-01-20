from django.conf.urls import url
from igenapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
               #url(r'^$', views.index, name='index'),
               #url(r'(?P<tea>\w+)/$', views.insert, name='insert'),
    url(r'^(?P<owner_name>[\w-]+)/$', views.home, name='home'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/wiki/$', views.wiki, name='wiki'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/wiki-form/$', views.wiki_form, name='wiki-form'),
    url(r'^issues/$', views.issues, name='issues'),
    url(r'^issue/(?P<issue_id>\d+)/$', views.new_issue, name='new_issue'),
    url(r'^add_issue/(?P<issue_id>\d+)/$', views.add_issue, name='add_issue'),
    url(r'^issues/(?P<issue_id>\d+)/$', views.issue_details, name='issue_details'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/commits/$', views.commits, name='commits'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/commit/(?P<commit_id>[\w-]+)/$', views.commit, name='commit'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/selected_branch/$', views.selected_branch, name='selected_branch'),
    url(r'^^(?P<owner_name>[\w-]+)/repositories/$', views.repositories, name='repositories'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/profile/$', views.editUser, name='editUser'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout')
              ]

