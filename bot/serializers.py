from rest_framework import serializers

from bot.models import TgUser


class BotVerifySerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # password = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TgUser
        fields = "__all__"
        read_only_fields = ("id", "chat_id", "user_ud", "username", "user")
        # fields = ('username', 'email', 'password')  #
        # extra_kwargs = {'email': {'required': False}}

    # def validate(self, attrs):
    #     user = authenticate(**attrs)
    #     if user and user.is_active:
    #         return user
    #     raise serializers.ValidationError("Incorrect Credentials")
