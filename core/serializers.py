from django.contrib.auth import authenticate, login, password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from core.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_repeat')
        extra_kwargs = {'password': {'write_only': True,
                                     'validators': [password_validation.validate_password], }}

    def validate(self, attrs):
        if 'password_repeat' not in attrs:
            raise ValidationError({
                'password_repeat': ['This field is mandatory'],
            })
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')
        if password_repeat != password:
            raise ValidationError({
                'password_repeat': ['Passwords do not match'],
                'password': ['Passwords do not match'],
            })
        return super(RegisterSerializer, self).validate(attrs)

    def create(self, validated_data):
        user = Profile.objects.create_user(username=validated_data['username'],
                                           email=validated_data['email'],
                                           first_name=validated_data['first_name'],
                                           last_name=validated_data['last_name'],
                                           password=validated_data['password'])
        return user

    def check_email_unique(self, attrs):
        email = attrs['email']
        return False if Profile.objects.filter(email=email).exists() else True


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password')  #
        extra_kwargs = {'email': {'required': False}}

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])

    class Meta:
        model = Profile
        fields = ('id',
                  'old_password',
                  'new_password',)
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        user: Profile = self.instance
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'wrong old password'})
        return attrs

    def update(self, instance: Profile, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        login(self.context['request'], instance, backend='django.contrib.auth.backends.ModelBackend')
        return instance
