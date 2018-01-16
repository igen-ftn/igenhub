from django.conf.urls import url
from igenapp import views

urlpatterns = [
               #url(r'^$', views.index, name='index'),
               #url(r'(?P<tea>\w+)/$', views.insert, name='insert'),
    url(r'^$', views.home, name='home'),
    url(r'^wiki/$', views.wiki, name='wiki'),
    url(r'^issues/$', views.issues, name='issues'),
    url(r'^new_issue/$', views.new_issue, name='new_issue'),
    url(r'^add_issue/$', views.add_issue, name='add_issue'),
    url(r'^(?P<issue_id>\d+)/$', views.issue_details, name='issue_details'),
    url(r'^commits/$', views.commits, name='commits'),
              ]
