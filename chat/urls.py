from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.Chat),
    url(r'^users_on$', views.Users_on),
    url(r'^send_message$', views.Send_message),
    url(r'^get_message$', views.Get_message)
]
