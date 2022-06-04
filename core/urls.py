from django.urls import path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

from core.views import LogOutView, LoginAPI, PasswordAPI, ProfileAPI, RegisterAPI

users_router = SimpleRouter()
users_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path('logout/', LogOutView.as_view()),
    path('profile', ProfileAPI.as_view()),
    path('update_password', PasswordAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('signup', RegisterAPI.as_view()),
]
