from random import choices
from string import ascii_uppercase, digits, ascii_lowercase

from django.contrib.auth import get_user_model
from django.db import IntegrityError

from core.models import Chat
from core.utils import generate_random_integer


def generate_random_name():
    """
    Generates random string
    """
    return ''.join(choices(ascii_uppercase + digits + ascii_lowercase, k=10))


def create_dummy_user():
    username = generate_random_name()
    while True:
        try:
            return get_user_model().objects.create_user(
                username=username,
                email='{}@test.com'.format(username),
                password='secret123'
            )
        except IntegrityError:
            continue
        except Exception as exc:
            print(str(exc))
            break


def create_dummy_chat():
    while True:
        try:
            return Chat.objects.create(code=generate_random_integer(), name=generate_random_name())
        except IntegrityError:
            continue
        except Exception as exc:
            print(str(exc))
            break


def get_http_methods(client, without):
    methods = {client.get, client.delete, client.put, client.patch, client.trace, client.options, client.head}
    return methods.difference(without)


def method_tester(instance, without=None):
    if not without:
        without = set()
    instance.client.force_authenticate(instance.user)
    for func in get_http_methods(instance.client, without=without):
        response = func(instance.url)
        instance.assertEqual(response.status_code, 405)
