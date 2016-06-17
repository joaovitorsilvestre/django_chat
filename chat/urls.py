from django.conf.urls import url , include
from . import views

urlpatterns = [
    url(r'^$', views.Index),
    url(r'^users_on/$', views.Users_on),
    url(r'^messages_get/(?P<user>\w+)$', views.Messages_get),
    url(r'^messages_send/$', views.Messages_send),
]
