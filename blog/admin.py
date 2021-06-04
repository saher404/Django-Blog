from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from .models import Article
from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'pub_time')
    list_filter = ('pub_time',)


admin.site.register(Article, ArticleAdmin)


# 定义一个行内 admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'


# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
