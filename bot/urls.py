from django.urls import path

from bot.views import VerifyUser

urlpatterns = [
    path('verify', VerifyUser.as_view()),
]
