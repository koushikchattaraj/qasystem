from django.db import models
from django.db.models import fields
from rest_framework import serializers
from collections import OrderedDict, namedtuple 
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from .jwt_payload import jwt_payload_handler
from .models import (
    User,
    UserProfile,
)


from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from uuid import uuid4
import base64
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate
from .backend import EmailBackend
JWT_PAYLOAD_HANDLER = jwt_payload_handler
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER



class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=120, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password, is_active="True")
        if user.is_active:
            if user is None:
                raise serializers.ValidationError(
                    'A user with this email and password is not found.'
                )
            try:
                payload = JWT_PAYLOAD_HANDLER(user)
                jwt_token = JWT_ENCODE_HANDLER(payload)
                update_last_login(None, user)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )
            return {
                'email':user.email,
                'token': jwt_token
            }
        else:
            raise serializers.ValidationError(
                    'please verify your email'
                )

class UserCreateSerilizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()
    # class Meta:
    #     model = User
    #     fields = ['id','email','password','name']
    def create(self, validated_data):
        email = validated_data.get('email')
        name = validated_data.get('name')
        user = User(email=email, username=email, name=name, is_active="False")
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UserSerilizers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'name']


class UserProfileSerilizer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'image', 'votes', 'token', 'is_active']

    
