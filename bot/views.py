import logging

from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import BotVerifySerializer
from core.models import Profile


class VerifyUser(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BotVerifySerializer
    queryset = TgUser.objects.all()

    def patch(self, request, *args, **kwargs):
        user = Profile.objects.get(username=request.user.username)
        try:
            tg_user = TgUser.objects.get(verification_code=request.data.get("verification_code", 'empty_code'))
        except TgUser.DoesNotExist:
            tg_user = None

        if tg_user: #.user_ud:
            logging.info(f'tg_user - {tg_user}')
            logging.info(f'user - {user}')
            logging.info(f'tg_user.user - {tg_user.user}')
            logging.info(f'user.id - {user.id}')
            print(f'tg_user - {tg_user}')
            print(f'user - {user}')
            print(f'tg_user.user - {tg_user.user}')
            print(f'user.id - {user.id}')
            tg_user.user = user
            tg_user.save()
            return Response({
                "success": "you've link your telegram user to your app user"
            }, 201)
        return Response({
            "error": "no user match verification code"
        }, 400)
        # return self.partial_update(request, *args, **kwargs)
