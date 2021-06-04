from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import models
from django import forms  # 导入表单
from django.contrib import auth
from django.contrib.auth.models import User  # 导入django自带的user表
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . import models
from .models import VisitNumber, Aimg
from .forms import AddForm
from .forms import ProfileForm
from .models import Profile
from django.db.models import Q


# 有文章搜索功能
def index(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'views':
            # 用 Q对象 进行联合搜索
            article_list = models.Article.objects.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            ).order_by('views')
        else:
            article_list = models.Article.objects.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'views':
            article_list = models.Article.objects.all().order_by('-views')
        else:
            article_list = models.Article.objects.all().order_by('-created')
    # 修改变量名称（articles -> article_list）
    # article_list = models.Article.objects.all()
    # 每页显示 10 篇文章
    paginator = Paginator(article_list, 10)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    views = VisitNumber.objects.filter(id=1)
    if views:
        views = views[0]
        views.count += 1
    else:
        views = VisitNumber()
        views.count = 1
    views.save()
    if not request.user.is_authenticated:
        return render(request, 'blog/blog.html',
                      {'articles': articles, 'views': views, 'order': order, 'search': search})
    if Profile.objects.filter(user_id=request.user.id).exists():  # filer若是查询不到数据，会返回一个空的查询集，[]  type类型是：Queryset。
        profile = Profile.objects.get(user_id=request.user.id)
        return render(request, 'blog/blog.html',
                      {'articles': articles, 'views': views, 'order': order, 'profile': profile, 'search': search})
    return render(request, 'blog/blog.html', {'articles': articles, 'views': views, 'order': order, 'search': search})


# 无文章搜索功能
# def index(request):
#     if request.GET.get('order') == 'views':
#         article_list = models.Article.objects.all().order_by('-views')
#         order = 'views'
#     else:
#         article_list = models.Article.objects.all().order_by('-created')
#         order = 'normal'
#     # 修改变量名称（articles -> article_list）
#     # article_list = models.Article.objects.all()
#     # 每页显示 10 篇文章
#     paginator = Paginator(article_list, 10)
#     # 获取 url 中的页码
#     page = request.GET.get('page')
#     # 将导航对象相应的页码内容返回给 articles
#     articles = paginator.get_page(page)
#     views = VisitNumber.objects.filter(id=1)
#     if views:
#         views = views[0]
#         views.count += 1
#     else:
#         views = VisitNumber()
#         views.count = 1
#     views.save()
#     if not request.user.is_authenticated:
#         return render(request, 'blog/blog.html', {'articles': articles, 'views': views, 'order': order})
#     if Profile.objects.filter(user_id=request.user.id).exists():  # filer若是查询不到数据，会返回一个空的查询集，[]  type类型是：Queryset。
#         profile = Profile.objects.get(user_id=request.user.id)
#         return render(request, 'blog/blog.html',
#                       {'articles': articles, 'views': views, 'order': order, 'profile': profile})
#     return render(request, 'blog/blog.html', {'articles': articles, 'views': views, 'order': order})


# 显示文章页面
def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    user_id = article.author
    article.views = article.views + 1
    article.save()
    if Profile.objects.filter(user_id=user_id).exists():
        profile = Profile.objects.get(user_id=user_id)
        return render(request, 'blog/article_page.html', {'article': article, 'profile': profile})
    return render(request, 'blog/article_page.html', {'article': article})


# 显示文章编辑页面
def edit_page(request, article_id):
    if not request.user.is_authenticated:
        return render(request, 'blog/notlogin.html')
    if str(article_id) == '0':
        return render(request, 'blog/edit_page.html')
    article = models.Article.objects.get(pk=article_id)
    # content_form = ArticleForm()
    return render(request, 'blog/edit_page.html', {'article': article})


# 文章编辑页面提交后返回主页面
def edit_action(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    article_id = request.POST.get('article_id', '0')
    # 新建文章时，article——id为0
    if article_id == '0':
        models.Article.objects.create(title=title, content=content, author=User.objects.get(id=request.user.id))
        response = redirect('/blog/blog')
        return response
    article = models.Article.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.save()
    response = redirect('/blog/blog')
    return response


def aimg(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    # 判断是否为 post 方法提交
    if request.method == "POST":
        af = AddForm(request.POST, request.FILES)
        # 判断表单值是否和法
        if af.is_valid():
            name = af.cleaned_data['name']
            articleimg = af.cleaned_data['articleimg']
            article.name = name
            article.articleimg = articleimg
            article.save()
            return render(request, 'blog/article_page.html', context={"aimg": aimg, 'article': article})
    else:
        af = AddForm()
        return render(request, 'blog/aimg.html', context={"af": af})


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密_码', widget=forms.PasswordInput())
    # Django的form的作用：
    # 1、生成html标签
    # 2、用来做用户提交的验证
    # Form的验证思路
    # 前端：form表单
    # 后台：创建form类，当请求到来时，先匹配，匹配出正确和错误信息


# 编辑用户信息
@login_required(login_url='/blog/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            # 带参数的 redirect()
            return redirect("blog:uedit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        user = User.objects.get(id=id)
        articles = models.Article.objects.filter(author_id=id)
        context = {'profile_form': profile_form, 'profile': profile, 'user': user, 'articles': articles}
        return render(request, 'blog/uedit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 个人空间
def space(request, id):
    profile = Profile.objects.get(user_id=id)
    articles = models.Article.objects.filter(author_id=id)
    context = {'profile': profile, 'articles': articles}
    return render(request, 'blog/space.html', context)


def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)  # 包含用户名和密码
        if uf.is_valid():
            # 获取表单数据
            username = uf.cleaned_data['username']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = uf.cleaned_data['password']
            # 添加到数据库
            # registAdd = User.objects.get_or_create(username=username,password=password)
            registAdd = User.objects.create_user(username=username, password=password)
            # print registAdd
            if registAdd == False:
                return render(request, 'blog/share1.html', {'registAdd': registAdd, 'username': username})

            else:
                # return HttpResponse('ok')
                return render(request, 'blog/share1.html', {'registAdd': registAdd})
                # return render_to_response('share.html',{'registAdd':registAdd},context_instance = RequestContext(request))
    else:
        # 如果不是post提交数据，就不传参数创建对象，并将对象返回给前台，直接生成input标签，内容为空
        uf = UserForm()
    # return render_to_response('regist.html',{'uf':uf},context_instance = RequestContext(request))
    return render(request, 'blog/regist1.html', {'uf': uf})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        re = auth.authenticate(username=username, password=password)  # 用户认证
        if re is not None:  # 如果数据库里有记录（即与数据库里的数据相匹配或者对应或者符合）
            auth.login(request, re)  # 登陆成功
            return redirect('/blog/blog', {'user': re})  # 跳转--redirect指从一个旧的url转到一个新的url
        else:  # 数据库里不存在与之对应的数据
            return render(request, 'blog/login.html', {'login_error': '用户名或密码错误'})  # 注册失败
    return render(request, 'blog/login.html')


def article_delete(request, article_id):
    if not request.user.is_authenticated:
        return render(request, 'blog/notlogin.html')
    # 根据 id 获取需要删除的文章
    article = models.Article.objects.get(pk=article_id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect('/blog/blog')


def logout(request):
    auth.logout(request)
    return render(request, 'blog/blog.html')


def vlogin(request):
    if not request.user.is_authenticated:
        return render(request, 'blog/notlogin.html')
    return redirect('/picture/')


def happybd(requset):
    return render(requset, 'blog/BirthdayCake.html')


def happybd1(requset):
    return render(requset, 'blog/Memories.html')


def video(request):
    return render(request, 'blog/video.html')


def tools(request):
    return render(request, 'blog/Tools.html')


def jsdemo(request):
    return render(request, 'blog/JSdemo.html')


def game1(request):
    return render(request, 'blog/game1.html')


# 实验室招新用
def zx(request):
    return render(request, 'blog/zx.html')


def qr(request):
    views = VisitNumber.objects.filter(id=1)
    if views:
        views = views[0]
        views.count += 1
    else:
        views = VisitNumber()
        views.count = 1
    views.save()
    return render(request, 'blog/QR.html', {'views': views})


#大创车联网用
def carlo(request):
    return render(request, 'blog/lo.html')


def car(request):
    return render(request, 'blog/dt.html')
