
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^$', views.signin),
    url(r'^register$', views.register),
    url(r'^register/process$', views.add),
    url(r'^secrets$',views.secretindex),
    url(r'^secrets/new$',views.addsecret),
    url(r'^secrets/all$',views.popular),
    url(r'^secrets/(?P<postid>\d+)/(?P<userid>\d+)$', views.like)
]