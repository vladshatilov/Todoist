from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(username=validated_data['username'],
                                           email=validated_data['email'],
                                           first_name=validated_data['first_name'],
                                           last_name=validated_data['last_name'],
                                           phone=validated_data['phone'],
                                           password=validated_data['password'])
        return user

    def check_email_unique(self, attrs):
        email = attrs['email']
        return False if Profile.objects.filter(email=email).exists() else True


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password')

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserDetailSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # email = serializers.CharField()
    # password = serializers.CharField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    # def update(self, request, *args, **kwargs):
    #     # print(f'2- {request.user.username}')
    #     email = request.data['email']
    #     # if Profile.objects.filter(username=request.user).exists()
    #     # instance = get_object_or_404(Profile, username=request.data.username)
    #     # validated_data = request.data
    #     instance.username = request.data.get('username', instance.username)
    #     instance.first_name = request.data.get('first_name', instance.first_name)
    #     instance.last_name = request.data.get('last_name', instance.last_name)
    #     instance.email = request.data.get('email', instance.email)
    #     # # instance.set_password(validated_data.get('password', instance.password))
    #     instance.save()
    #     return instance


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('password',)

