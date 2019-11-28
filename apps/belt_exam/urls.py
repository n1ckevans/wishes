from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^wishes$', views.wishes),
    url(r'^wishes/new$', views.new_wish),
    url(r'^make_wish$', views.make_wish),
    url(r'^cancel$', views.cancel),
    url(r'^wishes/remove/(?P<wish_id>\d+)$', views.remove),
    url(r'^wishes/edit/(?P<wish_id>\d+)$', views.edit),
    url(r'^wishes/edit_wish/(?P<wish_id>\d+)$', views.edit_wish),
    url(r'^wishes/granted/(?P<wish_id>\d+)$', views.granted),
    url(r'^stats$', views.stats),
    url(r'^wish/like/(?P<wish_id>\d+)$', views.wishes_like),
]