from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

users_router = SimpleRouter()
users_router.register("users", UserViewSet, basename="users")

# DATABASE_URL=psql://:@:/
#  Скрыть поле Password.
#  Сделать поля неизменяемыми: Last login, Date joined.

urlpatterns = [
    path("", include(users_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view()),
]
