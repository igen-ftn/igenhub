from django.conf.urls import url
from igenapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
               #url(r'^$', views.index, name='index'),
               #url(r'(?P<tea>\w+)/$', views.insert, name='insert'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/wiki/$', views.wiki, name='wiki'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/wiki-form/$', views.wiki_form, name='wiki-form'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/wiki-page/(?P<wikipage_id>\d+)/$', views.wiki_page, name='wiki-page'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/wiki-remove/(?P<wikipage_id>\d+)/$', views.remove_wikipage, name='remove-wikipage'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/wiki-edit/(?P<wikipage_id>\d+)/$', views.edit_wikipage, name='edit-wikipage'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/issues/$', views.issues, name='issues'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/issue/(?P<issue_id>\d+)/$', views.new_issue, name='new_issue'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/add_issue/(?P<issue_id>\d+)/$', views.add_issue, name='add_issue'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/issues/(?P<issue_id>\d+)/$', views.issue_details, name='issue_details'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/issues/search/$', views.search, name='search'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/issues/close/(?P<issue_id>\d+)/$', views.close, name='close'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/milestones/$', views.milestones, name='milestones'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/add_milestone/$', views.add_milestone, name='add_milestone'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/milestones/(?P<milestone_id>\d+)/$', views.remove_milestone, name='remove_milestone'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/labels/$', views.labels, name='labels'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/add_label/$', views.add_label, name='add_label'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/labels/(?P<label_id>\d+)/$', views.remove_label, name='remove_label'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/commits/$', views.commits, name='commits'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/commit/(?P<commit_id>[\w-]+)/$', views.commit, name='commit'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/selected_branch/$', views.selected_branch, name='selected_branch'),
    url(r'^^(?P<owner_name>[\w-]+)/repositories/$', views.repositories, name='repositories'),
    url(r'^^(?P<owner_name>[\w-]+)/new_repository/$', views.new_repository, name='new_repository'),
    url(r'^^(?P<owner_name>[\w-]+)/add_repository/$', views.add_repository, name='add_repository'),
    url(r'^^(?P<owner_name>[\w-]+)/repository/delete/(?P<repository_id>\d+)/$', views.delete_repository, name='delete_repository'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/(?P<parent>[\w-]+)/(?P<parent_id>\d+)/comments/$', views.add_comment, name='add_comment'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/(?P<parent>[\w-]+)/(?P<parent_id>\d+)/comments/edit/$', views.edit_comment, name='edit_comment'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/(?P<parent>[\w-]+)/(?P<parent_id>\d+)/comments/delete/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/graphs/$', views.graphs, name='graphs'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^accounts/profile/$', views.editUser, name='editUser'),
    url(r'^accounts/profile/removeAvatar', views.remove_avatar, name='remove_avatar'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^$', views.home, name='home'),
    url(r'^(?P<owner_name>[\w-]*)/$', views.home, name='home'),
    url(r'^(?P<owner_name>[\w-]+)/(?P<repo_name>[\w-]+)/$', views.landing, name='landing')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
