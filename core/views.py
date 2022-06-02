import os

from django.http import JsonResponse
from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.utils import json
from rest_framework.views import APIView

from core.permissions import IsAdminOrOwner, UserAccessPermission
from core.serializers import LoginSerializer, PasswordSerializer, RegisterSerializer, UserDetailSerializer, \
    UserSerializer

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, SlidingToken, UntypedToken
from core.models import Profile
from django.contrib.auth.hashers import check_password, make_password


def get(request):
    return JsonResponse({"status": "ok"}, status=200)

class RegisterAPI(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    # def post(self, request, *args, **kwargs):
    #     if 'password_repeat' not in request.data:
    #         raise ValidationError({
    #             'password_repeat': ['This field is mandatory'],
    #         })
    #     # password_repeat = request.data.pop('password_repeat', None)
    #     serializer = self.get_serializer(data=request.data)
    #
    #     error_dict = {}
    #     if not serializer.check_email_unique(request.data):
    #         error_dict['email'] = "Email exists"
    #     check_serializer = serializer.is_valid(raise_exception=True)
    #     if len(error_dict) == 0 and check_serializer:
    #         user = serializer.save()
    #         user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
    #         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    #         # user = User.objects.first()
    #         # SlidingToken.for_user(user)
    #         # RefreshToken.for_user(user)
    #         # str(RefreshToken.for_user(user))
    #         # str(RefreshToken.for_user(user).access_token)
    #         # return Response({
    #         #     # "user": UserSerializer(user, context=self.get_serializer_context()).data,
    #         #     # UserSerializer(user, context=self.get_serializer_context()).data,
    #         #     json.dumps(UserSerializer(user, context=self.get_serializer_context()).data), #, cls=UUIDEncoder
    #         #     # "access_token": str(AccessToken.for_user(user))
    #         # }, status=status.HTTP_201_CREATED)
    #         return self.post(request, *args, **kwargs)
    #     else:
    #         print(serializer.errors)
    #         error_dict["errors"] = serializer.errors
    #         return Response(error_dict, status=status.HTTP_403_FORBIDDEN)


# Login API
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data
        user = serializer.validate(request.data)
        print(user)
        print(request.data)
        print(serializer.data)
        if user is not None:
            login(request, user)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "access_token": str(AccessToken.for_user(user))
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "errors": serializer.errors
            })


# Profile API
class ProfileAPI(RetrieveUpdateDestroyAPIView):
    # permission_classes = [UserAccessPermission]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer
    queryset = Profile.objects.all()

    # @method_decorator(ensure_csrf_cookie)
    def get_object(self):
        return self.request.user

    # @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # @method_decorator(ensure_csrf_cookie)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # @method_decorator(ensure_csrf_cookie)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # @method_decorator(ensure_csrf_cookie)
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({
            "ok": "you've logged out"
        }, status=status.HTTP_204_NO_CONTENT)


# Password API
class PasswordAPI(UpdateAPIView):
    permission_classes = [UserAccessPermission]
    # model = Profile
    serializer_class = PasswordSerializer
    # lookup_field = 'username'
    queryset = Profile.objects.all()

    # MIN_LENGTH = 8
    #
    # def clean_new_password1(self):
    #     password1 = self.cleaned_data.get('new_password1')
    #
    #     # At least MIN_LENGTH long
    #     if len(password1) < self.MIN_LENGTH:
    #         raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)
    #
    #     # At least one letter and one non-letter
    #     first_isalpha = password1[0].isalpha()
    #     if all(c.isalpha() == first_isalpha for c in password1):
    #         raise forms.ValidationError("The new password must contain at least one letter and at least one digit or" \
    #                                     " punctuation character.")
    #
    #     return password1

    def get_object(self):
        return self.request.user

    # @method_decorator(ensure_csrf_cookie)
    def put(self, request, *args, **kwargs):
        user = Profile.objects.get(username=request.user.username)
        pwd_valid = check_password(request.data.get('old_password', 'None'+os.environ.get("SECRET_KEY", '5465487981625498')), user.password)

        if pwd_valid and request.data.get('new_password'):
            user.set_password(request.data.get('new_password'))
            user.save()
            # return self.update(request, *args, **kwargs)
            return Response({
                "ok": "you've changed your password"
            })
        else:
            return Response({
                "error": "wrong credentials"
            }, 400)

    # @method_decorator(ensure_csrf_cookie)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    # @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        logout(request)
        return Response({
            "ok": "you've logged out"
        })