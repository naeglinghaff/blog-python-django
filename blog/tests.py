from django.test import TestCase, RequestFactory
from mock import patch, MagicMock
import datetime
import pytz
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post
from .models import Comment
from .views import post_edit, post_new, post_remove, post_publish, add_comment_to_post, comment_approve, comment_remove, post_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

class TestBlogViews(TestCase):
    def setUp(self):
        client = Client()
        self.factory = RequestFactory()
        self.user = User(id = 1, is_superuser = 1, username = "naeglinghaff")
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="naeglinghaff", password="12345")
        self.comment = Comment(id = 1, author = 1, post_id = 1)
        self.comment.save()
        self.post = Post(title = 'My Post', text = 'This is some text', author_id = 1)
        self.post.save()

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

    def test_post_request_for_post_edit_function(self):
        data = {
            'title': "my edited post",
            'text': "my edited post text",
            'author_id': 1
        }
        request = self.factory.post("/post/1/edit/", data)
        request.user = self.user

        response = post_edit(request, pk = 1)
        self.assertEqual(response.status_code, 302)

    def test_blog_post_new_view_returns_200(self):
        request = self.factory.get("/post/new/")
        request.user = self.user

        response = post_new(request)

        self.assertEqual(response.status_code, 200)

    def test_post_request_for_post_new_function(self):
        data = {
            'title': "my new post",
            'text': "my new post text",
            'author_id': 1
        }
        request = self.factory.post("/post/new/", data)
        request.user = self.user

        response = post_new(request)
        self.assertEqual(response.status_code, 302)

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

    def test_blog_approve_comment_returns_302(self):
        request = self.factory.get("/comment/1/approve/")
        request.user = self.user

        response = comment_approve(request, pk = 1)

        self.assertEqual(response.status_code, 302)

    def test_blog_comment_remove_returns_302(self):
        request = self.factory.get("/comment/1/remove/")
        request.user = self.user

        response = comment_remove(request, pk = 1)

        self.assertEqual(response.status_code, 302)

    def test_no_posts_paginator_has_a_page_by_default(self):
        self.post.delete()
        response = self.client.get("//")
        posts = response.context[-1]['posts']
        page = posts.paginator.page(1)

        self.assertEqual(page.has_other_pages(), False)

    # def test_paginator_raises_empty_page_exception(self):
    #     with self.assertRaises(PageNotAnInteger):
    #         self.post.delete()
    #
    #         request = self.factory.get("//")
    #         post_list(request)


class TestBlogPostModel(TestCase):
    def setUp(self):
        self.user = User(id = 1, is_superuser = 1, username = "naeglinghaff")
        self.user.set_password("12345")
        self.user.save()
        self.timezone = pytz.timezone("GMT")

    def test_post_model_returns_string_title(self):
        post = Post(title="hello", text="This is some text")
        self.assertEqual(str(post), post.title)

    def test_post_model_retrieves_approved_comments(self):
        post = Post(title="hello", text="This is some text", author_id = 1)
        post.publish()
        comment = Comment(id = 1, author = 1, post_id = 1, text="this is a comment", approved_comment = True)
        comment.save()
        result = post.approved_comments()
        self.assertEqual(result[0], comment)

    def test_post_model_does_not_fetch_unapproved_comments(self):
        post = Post(title="hello", text="This is some text", author_id = 1)
        post.publish()
        comment = Comment(id = 1, author = 1, post_id = 1, text="this is a comment")
        comment.save()
        self.assertEqual(post.approved_comments().count(), 0)

    def test_post_model_publish_save_to_db_save_timestamp(self):
        with patch.object(timezone, 'now', return_value=self.timezone.localize(datetime.datetime(2020, 1, 1, 11, 00))) as mock_now:
            post = Post(title="hello", text="This is some text", author_id = 1)
            post.publish()
            self.assertEqual(Post.objects.count(), 1)
            self.assertEqual(post.published_date, self.timezone.localize(datetime.datetime(2020, 1, 1, 11, 0)))

    def test_creation_model_post(self):
        post = Post(title="hello", text="This is some text", author_id = 1)
        post.save()
        allposts = Post.objects.all()
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(allposts[0].text, "This is some text")
        self.assertIsInstance(allposts[0].created_date, datetime.date)
        self.assertIsInstance(allposts[0].author, User)

    def test_delete_method_deletes_post(self):
        post = Post(title="hello", text="This is some text", author_id = 1)
        post.save()
        post.delete()
        self.assertEqual(Post.objects.count(), 0)

class TestBlogCommentModel(TestCase):
    def setUp(self):
        self.user = User(id = 1, is_superuser = 1, username = "naeglinghaff")
        self.user.set_password("12345")
        self.user.save()
        self.post = Post(title="hello", text="This is some text", author_id = 1)
        self.post.save()
        self.comment = Comment(id = 1, author = 1, post_id = 1, text="this is a comment")
        self.comment.save()

    def test_comment_model_returns_string_title(self):
        self.assertEqual(str(self.comment), self.comment.text)

    def test_comment_approve_updates_approved_property(self):
        self.comment.approve()
        self.assertEqual(self.comment.approved_comment, True)
