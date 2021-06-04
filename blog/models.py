from __future__ import unicode_literals
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver
from django.db import models
from ckeditor.fields import RichTextField
# timezone 用于处理时间相关事务。
from django.utils import timezone


# 富文本


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    objects = models.Manager()
    title = models.CharField(max_length=32, default='article')
    # content = models.TextField(null=True)
    content = RichTextField(null=True)
    pub_time = models.DateTimeField(auto_now=True)  # 最后更新时间
    views = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50, blank=True)
    articleimg = models.FileField(upload_to="img/", blank=True)
    created = models.DateTimeField(default=timezone.now)  # 创建时间

    def __str__(self):
        return str(self.title)


class VisitNumber(models.Model):
    objects = models.Manager()
    count = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)


class Aimg(models.Model):
    name = models.CharField(max_length=50, blank=True)
    # upload_to 指定上传文件位置
    # 这里指定存放在 img/ 目录下
    articleimg = models.FileField(upload_to="img/", blank=True)

    # 返回名称
    def __str__(self):
        return str(self.name)


# 拓展用户信息---------
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# # 信号接收函数，每当新建 User 实例时自动调用
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# # 信号接收函数，每当更新 User 实例时自动调用
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# ----------------------------------
