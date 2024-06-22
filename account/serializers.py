from django.contrib.auth import authenticate

from rest_framework import serializers, exceptions

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', "phone", "password")

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def to_representation(self, instance):
        data = super(RegisterSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class LoginSerializer(TokenObtainPairSerializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone', None)
        password = attrs.get('password', None)

        user = authenticate(username=phone, password=password)

        if not user:
            raise exceptions.AuthenticationFailed('user not found')
        
        refresh_token = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh_token)
        attrs['access'] = str(refresh_token.access_token)
        attrs['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }
        return attrs
        
