from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    extra_kwargs = {
        'email': {'required': True},
        'password': {'required': True},
        'username': {'required': False},
        'first_name': {'required': False},
        'last_name': {'required': False},
    }


# class ProfileViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'first_name', 'last_name', 'email']
#         read_only_fields = ['email', 'first_name', 'last_name']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name']

    extra_kwargs = {
        'username': {'required': False},
        'first_name': {'required': False},
        'last_name': {'required': False},
    }