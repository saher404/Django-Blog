from django.conf.urls import url
from django.urls import path, re_path
from . import views
from tools.views import generate_qrcode

urlpatterns = [
    url(r'^qrcode/(.+)$', generate_qrcode, name='qrcode'),
]
