import random

from django.db import models

from core.models import Profile

CODE_VOCABULARY = "abcdefghijklmnoprqstuvwxyz123456789"

class TgUser(models.Model):
    class Meta:
        verbose_name = "tg user"
        verbose_name_plural = "tg users"

    chat_id = models.BigIntegerField(verbose_name="id", unique=True)
    user_ud = models.BigIntegerField(verbose_name="user_id")
    username = models.CharField(verbose_name="username", max_length=512, null=True, blank=True, default=None)
    user = models.ForeignKey(Profile, verbose_name="связанный пользователь", on_delete=models.PROTECT, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=32, verbose_name="verification_code_handler", null=True, blank=True)

    def set_verification_code(self):
        code = "".join([random.choice(CODE_VOCABULARY) for _ in range(12)])
        self.verification_code = code