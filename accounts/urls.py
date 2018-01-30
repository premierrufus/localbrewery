from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.accounts_list, name='accounts_list'),
    url(r'^new/$', views.account_new, name='account_new'),
    url(r'^accounts/(?P<pk>\d+)/$', views.account_detail, name='account_detail'),
]
