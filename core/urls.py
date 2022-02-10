from django.urls import path

from core import views


urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('chats/<int:chat_code>/exists', views.chat_exists, name='chat_exists'),
    path('chats/', views.CreateChatView.as_view(), name='create_chat'),
]
