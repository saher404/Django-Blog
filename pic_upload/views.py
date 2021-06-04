from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from .models import Picture
from . import models


# Create your views here.
class PicList(ListView):
    queryset = Picture.objects.all().order_by('-date')
    # ListView默认Context_object_name是object_list
    context_object_name = 'latest_picture_list'
    # 默认template_name = 'pic_upload/picture_list.html'


class PicDetail(DetailView):
    model = Picture


# DetailView默认Context_object_name是picture

# 下面是DetailView默认模板，可以换成自己的
# template_name = 'pic_upload/picture_detail.html'


class PicUpload(CreateView):
    model = Picture
    fields = ['title', 'image']
    # 可以通过fields选项自定义需要显示的表单


# CreateView默认Context_object_name是form。

# 下面是CreateView默认模板，可以换成自己模板
# template_name = 'pic_upload/picture_form.html'


def picture_delete(request, picture_id):
    if not request.user.is_authenticated:
        return render(request, 'blog/notlogin.html')
    picture = models.Picture.objects.get(pk=picture_id)
    picture.delete()
    return redirect('/picture')
