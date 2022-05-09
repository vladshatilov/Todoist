from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from core.views import LogOutView, LoginAPI, PasswordAPI, ProfileAPI, RegisterAPI

users_router = SimpleRouter()
users_router.register("users", UserViewSet, basename="users")
# users_router.register("core", UserViewSet, basename="core")

# DATABASE_URL=psql://:@:/
#  Скрыть поле Password.
#  Сделать поля неизменяемыми: Last login, Date joined.

urlpatterns = [
    # path("", include(users_router.urls)),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view()),
    path('core/login/', LoginAPI.as_view()),
    path('core/signup/', RegisterAPI.as_view()),
    path('core/logout/', LogOutView.as_view()),
    path('core/profile/<int:pk>', ProfileAPI.as_view()),
    path('core/update_password/', PasswordAPI.as_view()),
]
