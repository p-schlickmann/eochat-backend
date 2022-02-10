import logging

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=201, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        return instance


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
