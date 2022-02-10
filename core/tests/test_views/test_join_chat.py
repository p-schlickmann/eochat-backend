from json import loads
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.tests.utils import create_dummy_user, get_http_methods, create_dummy_chat, method_tester


class TestJoinChat(TestCase):
    def setUp(self):
        self.user = create_dummy_user()
        self.chat = create_dummy_chat()
        self.url = reverse('join_chat', args=[self.chat.code])
        self.client = APIClient()

    def test_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_new_member_can_join(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['joined'])

    def test_old_member_can_join(self):
        self.client.force_authenticate(self.user)
        self.client.post(self.url)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['joined'])

    @mock.patch('core.models.Chat.join')
    def test_error_handling(self, join_func):
        join_func.return_value = False
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['detail'], 'We had a problem trying to join this chat.')

    def test_invalid_chat_code(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('join_chat', args=[25336]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'Invalid chat code.')

    def test_only_post_allowed(self):
        method_tester(self, without={self.client.post, self.client.options})

