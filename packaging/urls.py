from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.packaging_list, name='packaging_list'),
    url(r'^new/$', views.packoff_new, name='packoff_new'),
    url(r'^packaging/(?P<pk>\d+)/$', views.packoff_detail, name='packoff_detail'),
]
