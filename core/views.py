import os

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from core.models import Profile
from core.permissions import UserAccessPermission
from core.serializers import LoginSerializer, PasswordSerializer, RegisterSerializer, UserDetailSerializer, \
    UserSerializer


def get(request):
    return JsonResponse({"status": "ok"}, status=200)

class RegisterAPI(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

# Login API
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validate(request.data)
        print(user)
        print(request.data)
        print(serializer.data)
        if user is not None:
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response({
            #     "user": UserSerializer(user, context=self.get_serializer_context()).data,
            #     "access_token": str(AccessToken.for_user(user))
            # }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "errors": serializer.errors
            })


# Profile API
class ProfileAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({
            "ok": "you've logged out"
        }, status=status.HTTP_204_NO_CONTENT)


# Password API
class PasswordAPI(UpdateAPIView):
    permission_classes = [UserAccessPermission]
    serializer_class = PasswordSerializer
    queryset = Profile.objects.all()


    def get_object(self):
        return self.request.user

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

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            "ok": "you've logged out"
        })