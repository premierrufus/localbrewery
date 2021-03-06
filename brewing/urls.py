from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.batch_list, name='batch_list'),
    url(r'^new/$', views.batch_new, name='batch_new'),
    url(r'^(?P<pk>\d+)/$', views.batch_detail, name='batch_detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.batch_edit, name='batch_edit'),
]
