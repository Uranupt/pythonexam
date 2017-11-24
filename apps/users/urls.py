from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.pokes, name="pokes"),
    url(r'^login$', views.logreg, name="logreg"),
    url(r'^loguser$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^addpokes$', views.addpoke, name="addpoke")
]
