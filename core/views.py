import os

from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView

from core.permissions import IsAdminOrOwner, UserAccessPermission
from core.serializers import LoginSerializer, PasswordSerializer, RegisterSerializer, UserDetailSerializer, \
    UserSerializer

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, SlidingToken, UntypedToken
from core.models import Profile
from django.contrib.auth.hashers import check_password, make_password


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        request.data.pop('password_repeat', None)
        serializer = self.get_serializer(data=request.data)

        error_dict = {}
        if not serializer.check_email_unique(request.data):
            error_dict['email'] = "Email exists"

        if len(error_dict) == 0 and serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # user = User.objects.first()
            # SlidingToken.for_user(user)
            # RefreshToken.for_user(user)
            # str(RefreshToken.for_user(user))
            # str(RefreshToken.for_user(user).access_token)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": str(AccessToken.for_user(user))
            })
        else:
            print(serializer.errors)
            error_dict["errors"] = serializer.errors
            return Response(error_dict)


# Login API
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data
        user = serializer.validate(request.data)
        print(request.data)
        if user is not None:
            login(request, user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": str(AccessToken.for_user(user))
            })
        else:
            return Response({
                "errors": serializer.errors
            })


# Profile API
class ProfileAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = [UserAccessPermission]
    serializer_class = UserDetailSerializer
    queryset = Profile.objects.all()

    @method_decorator(ensure_csrf_cookie)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({
            "ok": "you've logged out"
        })


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

    @method_decorator(ensure_csrf_cookie)
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

    @method_decorator(ensure_csrf_cookie)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# Get User API
class UserAPI(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)