from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Chat, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def update(self, instance, validated_data):
        """
        Update a user, setting the password, phone and cpf correctly
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ('code', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Message
        fields = ('author', 'content', 'created_at')
