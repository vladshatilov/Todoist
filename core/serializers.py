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
                                           # phone=validated_data['phone'],
                                           password=validated_data['password'])
        return user

    def check_email_unique(self, attrs):
        email = attrs['email']
        return False if Profile.objects.filter(email=email).exists() else True


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    # email = serializers.CharField()
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
    # username = serializers.CharField(allow_null=False, allow_blank=False)
    # email = serializers.CharField()
    # password = serializers.CharField(allow_null=False, allow_blank=False)

    class Meta:
        model = Profile
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        # fields = ('username', 'password')
        extra_kwargs = {
            'id': {'read_only': True},
        }

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
