from django.conf.urls import url
from address_book import views

urlpatterns = [
    # persons
    url(r'^persons/$', views.person_list),
    url(r'^persons/(?P<id>[0-9]+)/$', views.person_detail),
    url(r'^persons/find1/(?P<first_name>[a-zA-Z]+)/$', views.person_find1),
    url(r'^persons/find2/(?P<last_name>[a-zA-Z]+)/$', views.person_find2),
    url(r'^persons/find3/(?P<email>[a-zA-Z0-9\@\_\.]+)/$', views.person_find3),
    url(r'^persons/find/(?P<first_name>[a-zA-Z]+)/(?P<last_name>[a-zA-Z]+)/$', views.person_find),
    # groups
    url(r'^$', views.group_list),
    url(r'^groups/$', views.group_list),
    url(r'^groups/(?P<id>[0-9]+)/$', views.group_detail),
]
