from django.conf.urls import url
from igenapp import views

urlpatterns = [
               url(r'^$', views.index, name='index'),
               url(r'(?P<tea>\w+)/$', views.insert, name='insert'),
              ]