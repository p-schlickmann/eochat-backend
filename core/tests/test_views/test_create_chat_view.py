from json import loads

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.tests.utils import create_dummy_user, get_http_methods, method_tester


class TestCreateChatView(TestCase):
    def setUp(self):
        self.user = create_dummy_user()
        self.url = reverse('create_chat')
        self.client = APIClient()

    def test_authentication(self):
        response = self.client.post(self.url, {'name': 'newchat'})
        self.assertEqual(response.status_code, 401)

    def test_chat_creation(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, {'name': 'newchat2'})
        self.assertEqual(response.status_code, 201)
        response_content = loads(response.content)
        self.assertEqual(response_content['name'], 'newchat2')

    def test_only_post_allowed(self):
        method_tester(self, without={self.client.post, self.client.options})

