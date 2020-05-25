from django.test import TestCase, RequestFactory
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post
from .views import post_edit

class TestBlogViews(TestCase):
    def setUp(self):
        client = Client()
        self.factory = RequestFactory()
        self.user = User(id = 1, is_superuser = 1, username = "naeglinghaff", password = "fakepassword").save()
        post = Post(title = 'My Post', text = 'This is some text', author_id = 1).save()

    def test_homepage_can_render_posts(self):
        response = self.client.get("//")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_blog_detail_view_can_render(self):
        response = self.client.get("/post/1/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")

    def test_blog_edit_view_can_render(self):
        request = self.factory.get("/post/1/edit/")

        self.user = authenticate(username = "naeglinghaff", password = "fakepassword")

        request.user = self.user

        response = post_edit(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_edit.html")
