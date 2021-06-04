from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from myfuck.settings import MEDIA_ROOT
from . import views

app_name = 'blog'
urlpatterns = [
                  url(r'^blog/$', views.index, name='blog'),
                  url(r'^article/(?P<article_id>[0-9]+)$', views.article_page, name='article_page'),
                  url(r'^edit/(?P<article_id>[0-9]+)$', views.edit_page, name='edit_page'),
                  url(r'^edit/action$', views.edit_action, name='edit_action'),
                  url(r'^regist/$', views.regist, name='regist'),
                  url(r'^login/$', views.login, name='login'),
                  url(r'^logout/$', views.logout, name='logout'),
                  url(r'vlogin/$', views.vlogin, name='vlogin'),
                  url(r'bd/$', views.happybd, name='happybd'),
                  url(r'bd1/$', views.happybd1, name='happybd1'),
                  url(r'video/$', views.video, name='video'),
                  url(r'Tools/$', views.tools, name='Tools'),
                  url('article-delete/(?P<article_id>[0-9]+)$', views.article_delete, name='article_delete'),
                  url(r'QR/$', views.qr, name='qr'),
                  re_path('aimg/(?P<article_id>[0-9]+)/', views.aimg, name='aimg'),
                  url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
                  path('admin/', admin.site.urls),
                  path('uedit/<int:id>/', views.profile_edit, name='uedit'),
                  path('space/<int:id>/', views.space, name='space'),
                  path('jsdemo/', views.jsdemo, name='jsdemo'),
                  path('game1/', views.game1, name='game1'),
                  path('zx/', views.zx, name='zx'),
                  path('carlo/', views.carlo, name='carlo'),
                  path('car/', views.car, name='car')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
