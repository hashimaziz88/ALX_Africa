# accounts/serializers.py

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model().objects.create_user(username='admin', email='<EMAIL>', password='admin')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None),
        )
        Token.objects.create(user=user)  # Create a token for the new user
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        token, _ = Token.objects.get_or_create(user=user)
        return {'token': token.key}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']
