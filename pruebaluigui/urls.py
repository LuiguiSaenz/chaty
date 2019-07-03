"""pruebaluigui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from api.api_views import UserList, GameApiView, GameList, GameDetail, MoveApiView
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration', include('rest_auth.registration.urls')),
    url(r'^players/$', UserList.as_view()),
    url(r'^create-game/$', GameApiView.as_view()),
    url(r'^games/$', GameList.as_view()),
    url(r'^games/(?P<identifier>[0-9A-Za-z_\-]+)/$', GameDetail.as_view()),
    url(r'^games/(?P<identifier>[0-9A-Za-z_\-]+)/moves/$', MoveApiView.as_view()),
]
