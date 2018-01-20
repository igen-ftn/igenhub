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
    url(r'^issue/(?P<issue_id>\d+)/$', views.new_issue, name='new_issue'),
    url(r'^add_issue/(?P<issue_id>\d+)/$', views.add_issue, name='add_issue'),
    url(r'^issues/(?P<issue_id>\d+)/$', views.issue_details, name='issue_details'),
    url(r'^milestones/$', views.milestones, name='milestones'),
    url(r'^add_milestone/$', views.add_milestone, name='add_milestone'),
    url(r'^milestones/(?P<milestone_id>\d+)/$', views.remove_milestone, name='remove_milestone'),
    url(r'^labels/$', views.labels, name='labels'),
    url(r'^add_label/$', views.add_label, name='add_label'),
    url(r'^labels/(?P<label_id>\d+)/$', views.remove_label, name='remove_label'),
    url(r'^commits/$', views.commits, name='commits'),
    url(r'^commit/(?P<commit_id>\w+)/$', views.commit, name='commit'),
    url(r'^selected_branch/$', views.selected_branch, name='selected_branch'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/profile/$', views.editUser, name='editUser'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout')
              ]

