from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Article
from time import sleep
from django.urls import reverse


class ArticlePostViewTests(TestCase):

    def test_increase_views(self):
        # 请求详情视图时，阅读量 +1
        author = User(username='user4', password='test_password')
        author.save()
        article = Article(
            author=author,
            title='test4',
            content='test4',
        )
        article.save()
        self.assertIs(article.views, 0)

        url = reverse('blog:article_page', args=(article.id,))
        response = self.client.get(url)

        viewed_article = Article.objects.get(id=article.id)
        self.assertIs(viewed_article.views, 1)
