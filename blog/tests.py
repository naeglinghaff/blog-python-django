from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Post

class TestBlogViews(TestCase):
    def setUp(self):
        client = Client()
        author = User(id = 1, is_superuser = 1, username = "naeglinghaff")
        author.save()
        AUTH_USER_MODEL = author
        post = Post(title = 'My Post', text = 'This is some text', author_id = 1)
        post.save()

    def test_homepage_can_render_posts(self):
        response = self.client.get("//")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_blog_detail_view_can_render(self):
        response = self.client.get("/post/1/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
