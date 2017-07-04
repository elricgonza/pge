#!python
# log/urls.py
from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^recinto/(?P<pk>\d+)/$', views.recinto_detail, name='recinto_detail'),
    url(r'^categoria/new/$', views.categoria_new, name='categoria_new'),
    url(r'^search/$', views.search_page, name='search_page'),
]
