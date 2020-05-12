from django.test import TestCase
from django.test import Client

class TestPostList(TestCase):
    def setUp(self):
        client = Client()

    def test_homepage_can_render_posts(self):
        response = self.client.get("//")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")

        
