import json
import logging

from django.shortcuts import get_object_or_404
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


@api_view(['POST'])
def change_chat_name(request, chat_code):
    chat = get_object_or_404(Chat, code=int(chat_code))
    data = json.loads(request.body)
    try:
        chat.name = data['name']
        chat.save()
        return Response({'name': data['name']}, status=status.HTTP_200_OK)
    except:
        return Response({'detail': 'Problem trying to edit chat.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_chat(request, chat_code):
    chat = get_object_or_404(Chat, code=int(chat_code))
    try:
        chat.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({'detail': 'Problem trying to delete chat.'}, status=status.HTTP_400_BAD_REQUEST)
