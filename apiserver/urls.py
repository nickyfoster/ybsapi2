from django.conf.urls import url
from apiserver import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^users/$', views.users_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^test/', views.workload)
]

urlpatterns = format_suffix_patterns(urlpatterns)
