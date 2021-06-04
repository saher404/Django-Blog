from django.conf.urls import url
from . import views

app_name = 'qkl'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),

]
