from django.test import TestCase, RequestFactory
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post
from .models import Comment
from .views import post_edit, post_new, post_remove, post_publish, add_comment_to_post, comment_approve, comment_remove

class TestBlogViews(TestCase):
    def setUp(self):
        client = Client()
        self.factory = RequestFactory()
        self.user = User(id = 1, is_superuser = 1, username = "naeglinghaff")
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="naeglinghaff", password="12345")
        self.comment = Comment(id = 1, author = 2, post_id = 1)
        self.post = Post(title = 'My Post', text = 'This is some text', author_id = 1).save()

    def test_homepage_post_list_can_render_posts_(self):
        response = self.client.get("//")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_blog__post_detail_view_can_render(self):
        response = self.client.get("/post/1/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")

    def test_blog_post_edit_view_returns_200(self):
        request = self.factory.get("/post/1/edit/")

        request.user = self.user
        response = post_edit(request, pk = 1)

        self.assertEqual(response.status_code, 200)

    def test_blog_post_new_view_returns_200(self):
        request = self.factory.get("/post/new/")
        request.user = self.user

        response = post_new(request)

        self.assertEqual(response.status_code, 200)

    def test_blog_post_remove_view_returns_302(self):
        request = self.factory.get("/post/1/remove/")
        request.user = self.user

        response = post_remove(request, pk = 1)

        self.assertEqual(response.status_code, 302)

    def test_blog_post_publish_view_returns_302(self):
        request = self.factory.get("/post/1/publish/")
        request.user = self.user

        response = post_publish(request, pk = 1)

        self.assertEqual(response.status_code, 302)

    def test_blog_add_comment_to_post_returns_200(self):
        request = self.factory.get("/post/1/comment/")
        request.user = self.user

        response = add_comment_to_post(request, pk = 1)

        self.assertEqual(response.status_code, 200)
