from django.conf.urls import url
from apiserver import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    url(r'^users/$', views.users_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^test/$', views.workload),
    url(r'^healthCheck/$', views.health_check),
    url(r'^api-token-auth/', rest_views.obtain_auth_token),

]

urlpatterns = format_suffix_patterns(urlpatterns)
