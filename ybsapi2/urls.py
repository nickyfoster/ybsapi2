from django.urls import path, include

urlpatterns = [
    path('', include('apiserver.urls'))
]
