from django.conf.urls import url
from django.urls import path, re_path, include
from . import views, admin

app_name = 'wechat'

urlpatterns = [
    url(r'^$', views.weixin_main, name='weixin_main'),
    # url(r'^startmymenu$', views.startmymenu, name='startmymenu'),
]
