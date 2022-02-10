from rest_framework import status
from rest_framework.exceptions import APIException


class ChatDoesNotExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid chat code.'
    default_code = 'invalid_chat_code'
