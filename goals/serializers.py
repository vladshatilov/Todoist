from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, StringRelatedField

from core.serializers import UserDetailSerializer
from goals.models import Comment, Goal, GoalCategory


def category_validator(value: GoalCategory, user):
    if value.is_deleted:
        raise serializers.ValidationError("not allowed in deleted category")

    if value.user != user:
        raise serializers.ValidationError("not owner of category")
    return value


# GoalCategory
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


# Goal
class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def create(self, validated_data):
        category_item = validated_data.pop('category')
        validated_category_item = category_validator(category_item, self.context["request"].user)
        goal = Goal.objects.create(category_id=validated_category_item.id, **validated_data)
        return goal


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        # read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        category_validator(value, self.context["request"].user)


# Goal Comment
class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    # goal = PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")
