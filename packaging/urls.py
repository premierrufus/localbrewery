from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.packaging_list, name='packaging_list'),
    url(r'^packaging/(?P<pk>\d+)/$', views.packoff_detail, name='packoff_detail'),
    url(r'^brewing/(?P<pk>\d+)/$', views.batch_detail, name='batch_detail'),
]
