from django import forms
from .models import Profile, Article


# 表单类用以生成表单
class AddForm(forms.Form):
    name = forms.CharField()
    articleimg = forms.FileField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')


# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ('content',)
