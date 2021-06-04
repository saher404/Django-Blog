from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'pic_upload'
urlpatterns = [

    # 展示所有图片
    path('', views.PicList.as_view(), name='pic_list'),

    # 上传图片
    re_path(r'^pic/upload/$',
            views.PicUpload.as_view(), name='pic_upload'),
    # 展示图片
    re_path(r'^pic/(?P<pk>\d+)/$',
            views.PicDetail.as_view(), name='pic_detail'),
    re_path(r'^picdel/(?P<picture_id>\d+)/$', views.picture_delete, name='del'),
]
