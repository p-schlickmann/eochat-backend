import logging

from rest_framework import generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from core.models import Chat
from core.serializers import UserSerializer, ChatSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Responsible for creating users
    Overrides 'perform_create' to set password hash correctly
    """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Return auth token for user
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'patch', 'head', 'options')

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed


class CreateChatView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer


@api_view(['GET'])
def chat_exists(request, chat_code):
    try:
        Chat.objects.get(code=int(chat_code))
        return Response({'exists': True})
    except Exception:
        return Response({'exists': False})
