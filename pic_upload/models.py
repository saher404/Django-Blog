from django.db import models
from django.db import models
from datetime import date
from django.urls import reverse


# Create your models here.

class Picture(models.Model):
    objects = models.Manager()
    title = models.CharField("标题", max_length=100, blank=True, default='')
    image = models.ImageField("图片", upload_to="mypictures", blank=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.title

    # 对于使用Django自带的通用视图非常重要
    def get_absolute_url(self):
        return reverse('pic_upload:pic_detail', args=[str(self.id)])
