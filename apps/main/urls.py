from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^users/(?P<user_id>\d+)$', views.users),
    url(r'^newquote$', views.newquote),
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^logout$', views.logout),
]
