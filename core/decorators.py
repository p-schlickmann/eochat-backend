from django.core.handlers.wsgi import WSGIRequest
from rest_framework.exceptions import ParseError
from rest_framework.request import Request

from core.exceptions import ChatDoesNotExist
from core.models import Chat


def validate_chat(f):
    """
    Checks if chat exists and returns the chat instance
    """
    def wrap(*args, **kwargs):
        try:
            chat = Chat.objects.get(code=kwargs.get('chat_code'))
        except Chat.DoesNotExist:
            raise ChatDoesNotExist
        return f(args[0], chat)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap
