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
